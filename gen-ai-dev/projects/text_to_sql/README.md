# Text to SQL 
    
## Objective 
* This project aims to build RAG pipelines for retrieving data from any source of database and augment it to LLMs (like GCP models, GEMINI ect.,) to generate sql response 
* The sequence of propt templates are used to make the model learn more effectively 
* Finally, the generated sql query is fed into the database and output response from the database is obtained 
* Then this output result is generated in a natural languange prompt and is displayed in the streamlit application 

### StreamLit APP
* This project will have an end application using Streamlit, that will take the user queries as input in Natural Language and System response is generated in the natural language format 

## Limitation
* Chormadb is not supported because of the new version release. This FAISS is used for Vector db