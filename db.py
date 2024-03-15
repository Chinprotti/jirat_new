import streamlit as st
import psycopg2
import yaml

credentials = yaml.safe_load(open('./credentials.yaml'))

# Your Redshift connection credentials
cockroach_url = credentials['cockroach']['url']

def connect_to_cockroach():
    try:
        conn = psycopg2.connect(
            cockroach_url
            , sslmode='disable'
        )
        
        st.success("Connection Successful!")
        return conn
    except (Exception, psycopg2.Error) as error:
        st.error("Error while connecting to Redshift:", error)

def execute_sql_from_file(sql_file_path, data_tuple):
    """Executes SQL from a file with parameterized values."""
    conn = connect_to_cockroach()
    try:
        cursor = conn.cursor()

        with open(sql_file_path, 'r') as file:
            sql = file.read()
        cursor.execute(sql, data_tuple)
        conn.commit()
        st.success("Data inserted successfully!")

    except (Exception, psycopg2.Error) as error:
        st.error("Error executing SQL:")
        st.exception(error)
    finally:
        if conn:
            conn.close()