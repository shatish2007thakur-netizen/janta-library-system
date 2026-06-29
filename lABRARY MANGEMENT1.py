import streamlit as st
import pandas as pd

# Page Configuration & Styling
st.set_page_config(page_title="Janta Library Management System", layout="wide")

# Custom CSS for UI Colors (Matching your original pink & cyan theme)
st.markdown("""
    <style>
    .main-title {
        background-color: #2980b9;
        color: white;
        text-align: center;
        padding: 15px;
        font-size: 28px;
        font-weight: bold;
        border-radius: 5px;
        margin-bottom: 20px;
    }
    /* Sidebar layout color (Cyan background from your photo) */
    [data-testid="stSidebar"] {
        background-color: #00cecb;
        padding: 20px;
    }
    /* Label highlights (Pink blocks from your photo) */
    .pink-label {
        background-color: #ff65a3;
        color: black;
        font-weight: bold;
        padding: 4px 8px;
        border-radius: 3px;
        display: inline-block;
        margin-bottom: 5px;
    }
    /* Table header title (Blue banner) */
    .table-banner {
        background-color: #0066cc;
        color: white;
        text-align: center;
        padding: 8px;
        font-size: 18px;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Main Title Banner
st.markdown('<div class="main-title">SHREE JANTA SECONDARY SCHOOL LIBRARY MANAGEMENT SYSTEM</div>', unsafe_allow_html=True)

# Initialize Session State for holding data
if "books_df" not in st.session_state:
    st.session_state.books_df = pd.DataFrame([
        {"Book Name": "HP1", "Book ID": "0001", "Author": "JK Rowling", "Status of the Book": "Available", "Card ID of the Issuer": ""},
        {"Book Name": "Harry Potter 2", "Book ID": "0002", "Author": "JK Rowling", "Status of the Book": "Available", "Card ID of the Issuer": ""},
        {"Book Name": "Percy Jackson and the Olympians", "Book ID": "0103", "Author": "Rick Riordan", "Status of the Book": "Issued", "Card ID of the Issuer": "PG-10981"},
        {"Book Name": "Think Python", "Book ID": "1098", "Author": "Allen B. Downey", "Status of the Book": "Available", "Card ID of the Issuer": ""},
        {"Book Name": "Famous Five 1", "Book ID": "4567", "Author": "Enid Blyton", "Status of the Book": "Issued", "Card ID of the Issuer": "PG-1290"},
        {"Book Name": "Python GUI Programming", "Book ID": "8653", "Author": "Allen D. Moore", "Status of the Book": "Available", "Card ID of the Issuer": ""}
    ])

# --- LEFT SIDEBAR (Data Entry Form) ---
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

st.sidebar.markdown("<br>", unsafe_allow_html=True)

if st.sidebar.button("Add new record", use_container_width=True):
    if book_name and book_id:
        new_row = {
            "Book Name": book_name,
            "Book ID": book_id,
            "Author": author_name,
            "Status of the Book": status,
            "Card ID of the Issuer": card_id
        }
        st.session_state.books_df = pd.concat([st.session_state.books_df, pd.DataFrame([new_row])], ignore_index=True)
        st.sidebar.success("Record Added!")
    else:
        st.sidebar.error("Book Name & ID are required!")

# --- RIGHT SIDE PANEL (Controls & Table) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button("Delete Selected", use_container_width=True)
with col2:
    st.button("View record", use_container_width=True)
with col3:
    if st.button("Delete All Records", use_container_width=True):
        st.session_state.books_df = pd.DataFrame(columns=["Book Name", "Book ID", "Author", "Status of the Book", "Card ID of the Issuer"])
with col4:
    if st.button("Clear fields", use_container_width=True):
        st.rerun()

# Table Banner & Live Interactive Table
st.markdown('<div class="table-banner">INFORMATION ABOUT ALL THE BOOKS</div>', unsafe_allow_html=True)
st.data_editor(st.session_state.books_df, use_container_width=True, num_rows="dynamic")
