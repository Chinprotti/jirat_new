import streamlit as st
import psycopg2

# Your Redshift connection credentials
redshift_host = "your_redshift_host.redshift.amazonaws.com"
redshift_user = "your_redshift_user"
redshift_password = "your_redshift_password"

redshift_database = "your_redshift_database"
redshift_port = 5439  # Default Redshift port

def connect_to_redshift():
    try:
        conn = psycopg2.connect(
            host=redshift_host,
            port=redshift_port,
            database=redshift_database,
            user=redshift_user,
            password=redshift_password
        )
        return conn
    except (Exception, psycopg2.Error) as error:
        st.error("Error while connecting to Redshift:", error)

# Database page content
st.title("Database Connection")

conn = connect_to_redshift()

if conn:
    st.success("Successfully connected to Redshift!")