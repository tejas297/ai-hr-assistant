
1. Data extraction layer has been done
    extract the data from the pdfs and use fixed sized chunking strategy.
2. pgvector databased system running in docker using compose file. and enable the pgvector extension in postgrasql. 
   document_chunks table created in hr_assistant databse with init_db.py script.
3. after creating chunker we have created embedding which is use local embedded model to transform the text to vector embedding. we have test it successfully. now move to store embedded chunks in database. 
4. improve chunker with required metadata for chunks. created ingesion service which is our RAG ingestion pipeline. ok swo the records with embedding vector store in table succesfully, now we move to similarity search. now we are creating embedding from query and retrive similar chunks via sementic searching.
5. now we have test with three diffrent query, to decide threshold value. we have using the fiex-size chunk strategy. we can also implement the other stretagy to optimize chunks which impact on relevent chunks searching and give best semantically nearest chuncks to the query. here we use cosien distance formula to measure the similarity distance.
6. now we are moving the context builder which use to package those retrieval pieces so the LLM can understand exactly where they came from. so it return the context string which we can use for further processes. 
7. now we are moving to prompt construction.
8. the llm client has been created. now we have created rag service class which connect all pipeline components. it is orchestration function. congratulations! your core RAG pipeline developed and work end to end succesfully. also integrate with the fast api endpoint.
8. now we should make backend production-quality first. our next milestone is "error handling and clean dependency management".
9. now we create fakeLLM so while testing dont required to call real LLm model. 
10. so we are implementing the conversation history ,with two tables 1. conversations and 2. messages. the conversations table store session_id which refer to list of messages for that session.
