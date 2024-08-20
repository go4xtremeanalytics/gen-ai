import os
# from dotenv import load_dotenv

# load_dotenv()

# db_user = os.getenv("db_user")
# db_password = os.getenv("db_password")
# db_host = os.getenv("db_host")
# db_name = os.getenv("db_name")

# testing
db_user = "root"
db_password = "maniKANDAN-661"
db_host = "host.docker.internal" # Changed from "localhost"
db_name = "classicmodels"



# testing


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




from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
# from langchain.memory import ChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from sqlalchemy import *

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from table_details import table_chain as select_table
from prompts import final_prompt, answer_prompt
# from langchain_core.prompts import final_prompt, answer_prompt



########################################
from examples import get_example_selector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate

example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}\nSQLQuery:"),
        ("ai", "{query}"),
    ]
)

print(example_prompt)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    example_selector=get_example_selector(),
    # example_selector=  {
    #  'input':"what is price of `1968 Ford Mustang`",
    #  "query": "SELECT `buyPrice`, `MSRP` FROM products  WHERE `productName` = '1968 Ford Mustang' LIMIT 1;"   
    # },
    input_variables=["input","top_k"],
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries."),
        few_shot_prompt,
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]
)

answer_prompt = PromptTemplate.from_template(
    """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
SQL Query: {query}
SQL Result: {result}
Answer: """
)

#####################################################

import streamlit as st
# @st.cache_resource
def get_chain():
    print("Creating chain")
    
    
    
    # db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")

    # ######### New Code
    # import os
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ascendant-epoch-432900-m8-c87642eb57fa.json"


    ###############################   New   ###########################################################################################
    # Access the Google service account credentials
    service_account_info = st.secrets["gcp_service_account"]
    # Convert AttrDict to a regular dictionary
    service_account_dict = dict(service_account_info)

    # Create a temporary file and write the JSON data
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json", mode='w') as temp_file:
        json.dump(service_account_dict, temp_file)
        temp_file_path = temp_file.name

    print(f"Temporary file created at: {temp_file_path}")



    # Retrieve the JSON key file path from Streamlit Secrets


    # key_path = st.secrets["gcp_service_account"].get("path")

    # Set the environment variable to point to the key file
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path


    # Set the environment variable to point to the key file
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path


    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_file_path


    ##################################################################################################################################

   
    from langchain.agents.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
    from langchain.sql_database import SQLDatabase
    from langchain.llms import VertexAI
    PROJECT_ID = "ascendant-epoch-432900-m8"
    # REGION = "my_region" 
    dataset = "classicmodels"
    SQL_ALCHEMY_URL = f'bigquery://{PROJECT_ID}/{dataset}'
    db = SQLDatabase.from_uri(SQL_ALCHEMY_URL)



    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    generate_query = create_sql_query_chain(llm, db,final_prompt) 
    execute_query = QuerySQLDataBaseTool(db=db)
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    # chain = generate_query | execute_query
    chain = (
    RunnablePassthrough.assign(table_names_to_use=select_table) |
    RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
)

    return chain

def create_history(messages):
    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history

def invoke_chain(question,messages):
    chain = get_chain()
    history = create_history(messages)
    response = chain.invoke({"question": question,"top_k":3,"messages":history.messages})
    history.add_user_message(question)
    history.add_ai_message(response)
    return response
# messege = "Hi"
# def invoke_chain(messege):
#     print(messege)