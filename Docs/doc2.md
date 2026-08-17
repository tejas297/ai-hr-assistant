- we are not start with chatbot UI building, insted we are start with rag pipeline indexing part first :
```
PDF
 ↓
Python
 ↓
Extract text
 ↓
Chunks
 ↓
Embeddings
 ↓
pgvector
```
Then:
```
Question
 ↓
Embedding
 ↓
Vector search
 ↓
Relevant policy
```
Finally high level :
```
Relevant policy
       +
User question
       ↓
      LLM
       ↓
    Answer
```

- This is how RAG work internally.