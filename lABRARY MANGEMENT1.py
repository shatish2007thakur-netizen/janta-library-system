import streamlit as st
import pandas as pd
import requests

# Page Configuration
st.set_page_config(page_title="Janta Library Management System", layout="wide")

# Supabase API Details
SUPABASE_URL = "https://guoyvigqjbznsgjjizjs.supabase.co"
TABLE_URL = f"{SUPABASE_URL}/rest/v1/books"

# Supabase Key
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "sb_publishable_dmlrauPkLztOaJcqlnajfQ_g38HOONN")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# ==============================================================================
# --- 🔐 SESSION STATE & ADMIN ACCESS CONTROL ---
# ==============================================================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_role" not in st.session_state:
    st.session_state["user_role"] = "Guest"

st.sidebar.title("🔐 Access Control")

if not st.session_state["logged_in"]:
    login_type = st.sidebar.radio("Select View Mode", ["Public / Read-Only", "Admin Login"])
    
    if login_type == "Admin Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Login as Admin"):
            # Secrets se credentials match karega
            if "credentials" in st.secrets and username == st.secrets["credentials"]["admin_username"] and password == st.secrets["credentials"]["admin_password"]:
                st.session_state["logged_in"] = True
                st.session_state["user_role"] = "Admin"
                st.sidebar.success("Welcome Back, Admin!")
                st.rerun()
            else:
                st.sidebar.error("Invalid Username or Password!")
    else:
        st.sidebar.info("🌐 Status: Read-Only Mode (View Only)")
else:
    st.sidebar.write(f"Logged in as: **{st.session_state['user_role']}**")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user_role"] = "Guest"
        st.rerun()

st.sidebar.markdown("---")

# Helper function to enforce Admin Check
def is_admin():
    return st.session_state.get("user_role") == "Admin"

# Helper function to load data from Supabase
def load_data_from_supabase():
    try:
        response = requests.get(f"{TABLE_URL}?order=book_id.asc", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                df = df.rename(columns={
                    "book_name": "Book Name", 
                    "book_id": "Book ID", 
                    "author": "Author", 
                    "status": "Status of the Book", 
                    "card_id": "Card ID of the Issuer"
                })
                if "id" in df.columns: df = df.drop(columns=["id"])
                if "created_at" in df.columns: df = df.drop(columns=["created_at"])
                return df
        return pd.DataFrame(columns=["Book Name", "Book ID", "Author", "Status of the Book", "Card ID of the Issuer"])
    except Exception:
        return pd.DataFrame(columns=["Book Name", "Book ID", "Author", "Status of the Book", "Card ID of the Issuer"])

# --- UI Styling ---
st.markdown("""
    <style>
    .main-title { background-color: #2980b9; color: white; text-align: center; padding: 15px; font-size: 28px; font-weight: bold; border-radius: 5px; margin-bottom: 20px; }
    [data-testid="stSidebar"] { background-color: #00cecb; padding: 20px; }
    .pink-label { background-color: #ff65a3; color: black; font-weight: bold; padding: 4px 8px; border-radius: 3px; display: inline-block; margin-bottom: 5px; }
    .table-banner { background-color: #0066cc; color: white; text-align: center; padding: 8px; font-size: 18px; font-weight: bold; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">SHREE JANTA SECONDARY SCHOOL LIBRARY MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)

# Dataframe state setup
if "books_df" not in st.session_state:
    st.session_state.books_df = load_data_from_supabase()


# ==============================================================================
# --- 📝 SIDEBAR: BOOK DATA ENTRY (ADMIN ONLY) ---
# ==============================================================================
st.sidebar.subheader("➕ Add New Book")

if is_admin():
    st.sidebar.markdown('<p class="pink-label">Book Name</p>', unsafe_allow_html=True)
    book_name = st.sidebar.text_input("Book Name Input", label_visibility="collapsed")

    st.sidebar.markdown('<p class="pink-label">Book ID</p>', unsafe_allow_html=True)
    book_id = st.sidebar.text_input("Book ID Input", label_visibility="collapsed")

    st.sidebar.markdown('<p class="pink-label">Author Name</p>', unsafe_allow_html=True)
    author_name = st.sidebar.text_input("Author Name Input", label_visibility="collapsed")

    st.sidebar.markdown('<p class="pink-label">Status of the Book</p>', unsafe_allow_html=True)
    status = st.sidebar.selectbox("Status Dropdown", ["Available", "Issued"], label_visibility="collapsed")

    st.sidebar.markdown('<p class="pink-label">Issuer\'s Card ID</p>', unsafe_allow_html=True)
    card_id = st.sidebar.text_input("Card ID Input", label_visibility="collapsed")

    if st.sidebar.button("Add new record", use_container_width=True):
        if book_name and book_id:
            payload = {
                "book_name": book_name,
                "book_id": book_id,
                "author": author_name,
                "status": status,
                "card_id": card_id if status == "Issued" else ""
            }
            res = requests.post(TABLE_URL, headers=HEADERS, json=payload)
            if res.status_code in [200, 201]:
                st.sidebar.success("Saved to Cloud Database!")
                st.session_state.books_df = load_data_from_supabase()
                st.rerun()
            else:
                st.sidebar.error(f"Error Code: {res.status_code}. Database issue.")
        else:
            st.sidebar.error("Book Name & ID are required!")
else:
    st.sidebar.warning("🔒 Nayi books add karne ke liye Admin Login zaroori hai.")


# ==============================================================================
# --- ⚙️ CONTROLS & ACTION BUTTONS ---
# ==============================================================================
col1, col2, col3, col4 = st.columns(4)

# Action 1: Delete Single Record
with col1:
    delete_id = st.text_input("Enter Book ID to Delete", placeholder="Book ID...", label_visibility="collapsed")
    if st.button("Delete Selected ID", use_container_width=True):
        if not is_admin():
            st.error("🛑 Access Denied: Sirf Admin hi records delete kar sakta hai!")
        elif not delete_id:
            st.warning("Please type a Book ID first!")
        else:
            del_url = f"{TABLE_URL}?book_id=eq.{delete_id}"
            res = requests.delete(del_url, headers=HEADERS)
            if res.status_code in [200, 204]:
                st.success(f"Book {delete_id} deleted successfully!")
                st.session_state.books_df = load_data_from_supabase()
                st.rerun()
            else:
                st.error("Could not delete. Check ID.")

# Action 2: Refresh Data (Allowed for everyone)
with col2:
    if st.button("Refresh / View Records", use_container_width=True):
        st.session_state.books_df = load_data_from_supabase()
        st.rerun()

# Action 3: Clear All Records (Admin Only)
with col3:
    if st.button("Delete All Records", use_container_width=True):
        if not is_admin():
            st.error("🛑 Access Denied: Pure database ko clear karne ki permission sirf Admin ko hai!")
        else:
            truncate_headers = HEADERS.copy()
            truncate_headers["Prefer"] = "count=exact"
            res = requests.delete(f"{TABLE_URL}?book_id=neq.0", headers=truncate_headers)
            if res.status_code in [200, 204]:
                st.success("All data cleared from Supabase!")
                st.session_state.books_df = load_data_from_supabase()
                st.rerun()
            else:
                st.error("Failed to delete all records.")

# Action 4: Clear Input Fields
with col4:
    if st.button("Clear Input Fields", use_container_width=True):
        st.rerun()


# ==============================================================================
# --- 📊 LIVE SECURE TABLE VIEW ---
# ==============================================================================
st.markdown('<div class="table-banner">INFORMATION ABOUT ALL THE BOOKS (SECURE CLOUD DATABASE)</div>', unsafe_allow_html=True)

if not st.session_state.books_df.empty:
    st.dataframe(st.session_state.books_df, use_container_width=True)
else:
    st.info("Cloud database khali hai ya connect nahi ho raha.")
