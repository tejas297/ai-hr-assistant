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


##  we use cosine distance.

conceptually :

```
similarity(query, chunk)

        ↑
        │
        ├── 1.0 → very similar
        │
        ├── 0.5 → somewhat similar
        │
        └── 0.0 → very different
```


## user interaction flow :

```
                    USER
                      │
                      ▼
              "How many paid
               leaves do I get?"
                      │
                      ▼
              Query Embedding
                      │
                      ▼
              Vector Search
                      │
                      ▼
              Top-K HR Chunks
                      │
                      ▼
              Context Builder
                      │
                      ▼
              ┌───────────────┐
              │      LLM      │
              └───────┬───────┘
                      │
                      ▼
              Grounded Answer
                      │
                      ▼
                Source/Page
```



to access the database :
- psql -h localhost -U hr_user -d hr_assistant

to enable the vector extension :
- CREATE EXTENSION IF NOT EXISTS vector;

to run app 
- uvicorn app.main:app --reload

