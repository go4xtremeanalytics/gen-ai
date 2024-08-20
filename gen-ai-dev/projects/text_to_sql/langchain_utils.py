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

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
# LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# OPENAI_API_KEY="sk-proj-VofqaSNGH9176ePfZRg0T3BlbkFJQ5KchbPXWLVFfEhsxH4z"
# LANGCHAIN_TRACING_V2="true"
# LANGCHAIN_API_KEY="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"




import os
os.environ["OPENAI_API_KEY"] = "sk-proj-VofqaSNGH9176ePfZRg0T3BlbkFJQ5KchbPXWLVFfEhsxH4z"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"




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

    ######### New Code
    import os
    # gac = st.secrets["gcp_service_account"]
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = gac



    import google.auth
    from google.oauth2 import service_account
    from google.cloud import bigquery

    import streamlit as st
    import os
    import google.auth

    # Retrieve the JSON key file path from Streamlit Secrets
    key_path = st.secrets["google_key_path"]

    # Set the environment variable to point to the key file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

    import os
    os.environ["OPENAI_API_KEY"] = "sk-proj-VofqaSNGH9176ePfZRg0T3BlbkFJQ5KchbPXWLVFfEhsxH4z"
    # from sqlalchemy import *
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