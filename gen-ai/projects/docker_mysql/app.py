import os
import streamlit as st
import mysql.connector
import pandas as pd

# Database connection
@st.cache_resource
def init_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "host.docker.internal"), # Changed from 'localhost'
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "maniKANDAN-661"),
        database=os.getenv("MYSQL_DATABASE", "classicmodels")
    )

conn = init_connection()

# Perform query
@st.cache_data
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

# Streamlit app
st.title('My Streamlit App with MySQL Data')

# Example query
query = "SELECT customerNumber, customerName, phone FROM customers LIMIT 10"
rows = run_query(query)

# Display data
st.write("Data from MySQL:")
df = pd.DataFrame(rows, columns=["customerNumber", "customerName", "phone"])  # Replace with your actual column names
st.dataframe(df)
