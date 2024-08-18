import os
import streamlit as st
import mysql.connector
import pandas as pd

# Database connection
# This is for testing
db_config = st.secrets["connections"]["mysql"]




def create_connection():
    try:
        conn = mysql.connector.connect(
            host=db_config["host"],
            user=db_config["username"],
            password=db_config["password"],
            database=db_config["database"],
            port=db_config["port"]
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

# Query the database
def query_database(query):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    else:
        return None

# Example usage in Streamlit
st.title("MySQL Database Connection Example")

query = "SELECT customerNumber, customerName, phone FROM customers LIMIT 10;"
data = query_database(query)

if data:
    st.write(data)
else:
    st.write("No data found or error in connection.")


###############################################################################   END ######################################################################################################

# @st.cache_resource
# def init_connection():
#     return mysql.connector.connect(
#         host=os.getenv("MYSQL_HOST", 'localhost'), # Changed from "host.docker.internal" 
#         user=os.getenv("MYSQL_USER", "root"),
#         password=os.getenv("MYSQL_PASSWORD", "maniKANDAN-661"),
#         database=os.getenv("MYSQL_DATABASE", "classicmodels")
#     )



# Initialize connection.
# conn = st.connection('mysql', type='sql')

# Perform query.
# This is for testing
# df = conn.query('SELECT customerNumber, customerName, phone FROM customers LIMIT 10;', ttl=600)  



# conn = init_connection()

# Perform query
# @st.cache_data
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall()

# Streamlit app
# st.title('My Streamlit App with MySQL Data')

# Example query
# query = "SELECT customerNumber, customerName, phone FROM customers LIMIT 10"
# rows = run_query(query)

# Display data
# st.write("Data from MySQL:")
# df = pd.DataFrame(rows, columns=["customerNumber", "customerName", "phone"])  # Replace with your actual column names
# st.dataframe(df)
