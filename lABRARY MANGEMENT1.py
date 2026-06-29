import streamlit as st
import pandas as pd
import requests

# Page Configuration
st.set_page_config(page_title="Janta Library Management System", layout="wide")

# Please Give the details about your supabase
SUPABASE_URL = "https://guoyvigqjbznsgjjizjs.supabase.co"
SUPABASE_KEY = "sb_publishable_dmlrauPkLztOaJcqlnajfQ_g38HOONN"
TABLE_URL = f"{SUPABASE_URL}/rest/v1/books"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# Supabase
def load_data_from_supabase():
    try:
        response = requests.get(TABLE_URL, headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
               
                df = df.rename(columns={
                    "book_name": "Book Name", "book_id": "Book ID", 
                    "author": "Author", "status": "Status of the Book", 
                    "card_id": "Card ID of the Issuer"
                })
                #  Supabase 
                if "id" in df.columns: df = df.drop(columns=["id"])
                return df
        return pd.DataFrame(columns=["Book Name", "Book ID", "Author", "Status of the Book", "Card ID of the Issuer"])
    except:
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


if "books_df" not in st.session_state:
    st.session_state.books_df = load_data_from_supabase()


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
        # Supabase 
        payload = {
            "book_name": book_name,
            "book_id": book_id,
            "author": author_name,
            "status": status,
            "card_id": card_id
        }
        res = requests.post(TABLE_URL, headers=HEADERS, json=payload)
        if res.status_code in [200, 201]:
            st.sidebar.success("Saved to Cloud Database!")
            st.session_state.books_df = load_data_from_supabase()
            st.rerun()
        else:
            st.sidebar.error("Database Error! Check settings.")
    else:
        st.sidebar.error("Book Name & ID are required!")

# --- RIGHT SIDE PANEL 
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.button("Delete Selected", use_container_width=True)
with col2:
    st.button("View record", use_container_width=True)
with col3:
    if st.button("Delete All Records", use_container_width=True):
        requests.delete(TABLE_URL, headers={"apikey": SUPABASE_KEY, "Authorization": f"Bearer {SUPABASE_KEY}"})
        st.session_state.books_df = load_data_from_supabase()
        st.rerun()
with col4:
    if st.button("Clear fields", use_container_width=True):
        st.rerun()

st.markdown('<div class="table-banner">INFORMATION ABOUT ALL THE BOOKS (SECURE CLOUD DATABASE)</div>', unsafe_allow_html=True)
st.data_editor(st.session_state.books_df, use_container_width=True, num_rows="dynamic")
