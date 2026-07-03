import streamlit as st
import pandas as pd
import requests

# Page Configuration
st.set_page_config(page_title="Janta Library Management System", layout="wide")

# ⚠️ URL Fix kiya (Double /rest/v1/ hata diya)
SUPABASE_URL = "https://guoyvigqjbznsgjjizjs.supabase.co"
TABLE_URL = f"{SUPABASE_URL}/rest/v1/books"

# Supabase Ke Liye Zaroori Key
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", "sb_publishable_dmlrauPkLztOaJcqlnajfQ_g38HOONN")

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# Supabase se live data load karne ka function
def load_data_from_supabase():
    try:
        # Get request me parameters pass kiye taaki proper sorted data aaye
        response = requests.get(f"{TABLE_URL}?order=book_id.asc", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                # Frontend columns ko safe format me rakhein par 'book_id' database key track karne ke liye rakhein
                df = df.rename(columns={
                    "book_name": "Book Name", 
                    "book_id": "Book ID", 
                    "author": "Author", 
                    "status": "Status of the Book", 
                    "card_id": "Card ID of the Issuer"
                })
                # Extra internal database columns screen se hata dein
                if "id" in df.columns: df = df.drop(columns=["id"])
                if "created_at" in df.columns: df = df.drop(columns=["created_at"])
                return df
        return pd.DataFrame(columns=["Book Name", "Book ID", "Author", "Status of the Book", "Card ID of the Issuer"])
    except Exception as e:
        return pd.DataFrame(columns=["Book Name", "Book ID", "Author", "Status of the Book", "Card ID of the Issuer"])

# UI Custom Styling
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

# --- LEFT SIDEBAR (डेटा एंट्री) ---
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
            st.sidebar.error(f"Error Code: {res.status_code}. DB Connection Issue.")
    else:
        st.sidebar.error("Book Name & ID are required!")

# --- RIGHT SIDE PANEL (कंट्रोल्स और एक्शन्स) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    # Selected row delete karne ke liye input box
    delete_id = st.text_input("Enter Book ID to Delete", placeholder="Book ID...", label_visibility="collapsed")
    if st.button("Delete Selected ID", use_container_width=True):
        if delete_id:
            # Supabase me row delete karne ke liye filter url parameters bhejte hain
            del_url = f"{TABLE_URL}?book_id=eq.{delete_id}"
            res = requests.delete(del_url, headers=HEADERS)
            if res.status_code in [200, 204]:
                st.success(f"Book {delete_id} deleted successfully!")
                st.session_state.books_df = load_data_from_supabase()
                st.rerun()
            else:
                st.error("Could not delete. Check ID.")
        else:
            st.warning("Please type a Book ID first!")

with col2:
    if st.button("Refresh / View Records", use_container_width=True):
        st.session_state.books_df = load_data_from_supabase()
        st.rerun()

with col3:
    if st.button("Delete All Records", use_container_width=True):
        # Supabase bina filter ke sab delete nahi karne deta jab tak Preference header set na ho
        truncate_headers = HEADERS.copy()
        truncate_headers["Prefer"] = "count=exact"
        # Sabhi data clear karne ke liye eq.neq filter bypass lagaya hai
        res = requests.delete(f"{TABLE_URL}?book_id=neq.0", headers=truncate_headers)
        st.success("All data cleared from Supabase!")
        st.session_state.books_df = load_data_from_supabase()
        st.rerun()

with col4:
    if st.button("Clear Input Fields", use_container_width=True):
        st.rerun()

# --- LIVE SECURE TABLE VIEW ---
st.markdown('<div class="table-banner">INFORMATION ABOUT ALL THE BOOKS (SECURE CLOUD DATABASE)</div>', unsafe_allow_html=True)

if not st.session_state.books_df.empty:
    # Table data display karne ke liye
    st.dataframe(st.session_state.books_df, use_container_width=True)
else:
    st.info("Cloud database khali hai ya connect nahi ho raha. Sidebar se books add karein.")
