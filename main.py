import pandas as pd
import streamlit as st
import numpy as np
import joblib
import sklearn
import requests

# Load models
pipeline = joblib.load('models/pipeline_19.pkl')
imputer = joblib.load('models/imputer_3m.pkl')

import pages.database  # Import the 'database' page
import pages.v3_model  # Import the 'v3_model' page

# Sidebar Navigation
st.sidebar.title("Navigation")
selected_page = st.sidebar.selectbox("Select a page", ["Home", "V3 Model", "Database"])

# Conditionally render pages
if selected_page == "Home":
    st.title("Welcome!")  
    st.markdown("Select a page from the sidebar")

elif selected_page == "V3 Model":
    # Content from 'pages/v3_model.py' will render here
    pass 

elif selected_page == "Database":
    # Content from 'pages/database.py' will render here
    pass 