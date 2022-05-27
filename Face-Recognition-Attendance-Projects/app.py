

# app.py
from apps import Home,Hello,Test
import streamlit as st
PAGES = {
    "Home": Home,
    "Hello New User": Hello,
    "Test Model":Test
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
