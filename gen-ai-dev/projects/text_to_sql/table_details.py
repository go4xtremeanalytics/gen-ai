import pandas as pd
import streamlit as st
from operator import itemgetter
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
# import os
# os.environ["OPENAI_API_KEY"] = "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"
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = "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"


###############################   New   #################################################################

import streamlit as st
import os
import json
import tempfile

# Access the OpenAI API key
openai_api_key = st.secrets["api_keys"]["openai_api_key"]
import os
os.environ["OPENAI_API_KEY"] = openai_api_key

#################################################################

llm = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0)
from typing import List

# @st.cache_data
def get_table_details():
    # Read the CSV file into a DataFrame
    database_table_descriptions = {"Table": ["productlines", "products", "offices", "employees", "customers", "payments", "orders", "orderdetails"], 
                                   "Description": ["Stores information about the different product lines offered by the company, including a unique name, textual description, HTML description, and image. Categorizes products into different lines.", 
                                                   "Contains details of each product sold by the company, including code, name, product line, scale, vendor, description, stock quantity, buy price, and MSRP. Linked to the productlines table.", 
                                                   "Holds data on the company's sales offices, including office code, city, phone number, address, state, country, postal code, and territory. Each office is uniquely identified by its office code.", 
                                                   "Stores information about employees, including number, last name, first name, job title, contact info, and office code. Links to offices and maps organizational structure through the reportsTo attribute.", 
                                                   "Captures data on customers, including customer number, name, contact details, address, assigned sales rep, and credit limit. Central to managing customer relationships and sales processes.", 
                                                   "Records payments made by customers, tracking the customer number, check number, payment date, and amount. Linked to the customers table for financial tracking and account management.", 
                                                   "Details each sales order placed by customers, including order number, dates, status, comments, and customer number. Linked to the customers table, tracking sales transactions.", 
                                                   "Describes individual line items for each sales order, including order number, product code, quantity, price, and order line number. Links orders to products, detailing the items sold."]}
    table_description = pd.DataFrame(database_table_descriptions)
    # table_description = pd.read_csv("database_table_descriptions.csv")
    table_docs = []

    # Iterate over the DataFrame rows to create Document objects
    table_details = ""
    for index, row in table_description.iterrows():
        table_details = table_details + "Table Name:" + row['Table'] + "\n" + "Table Description:" + row['Description'] + "\n\n"

    return table_details


class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")

def get_tables(tables: List[Table]) -> List[str]:
    tables  = [table.name for table in tables]
    return tables


# table_names = "\n".join(db.get_usable_table_names())
table_details = get_table_details()
table_details_prompt = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables are:

{table_details}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

table_chain = {"input": itemgetter("question")} | create_extraction_chain_pydantic(Table, llm, system_message=table_details_prompt) | get_tables