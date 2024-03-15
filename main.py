import streamlit as st

from st_pages import show_pages_from_config, show_pages, Page

show_pages_from_config()


def home_page(): 
    st.title("Welcome!")  
    st.markdown("Select a page from the sidebar")

home_page()