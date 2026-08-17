
# RAG PIPELINE
- A RAG pipeline has two distinct phases that run at diffrent times: 
    an offline indexing phase that prepares your knowledge base,
    an online phase that runs every time a user asks something.

## 1. Indexing(done once, then updated periodically)

```
    Documents (PDFs, docs, web pages, tickets)
        |
        v
    Chunking (Split into overlapping passages)
        |
        v
    Embedding Model(Converts each chunk to a vector)
        |
        v
    Vector databse (Stores vectors for fast search)
```

## 2. Query time (runs on every user request)

```
    User query (A question in natural language)
        |
        v
    Embed query (same embedding model as indexing)
        |
        v
    Vector search (finds top-k most simillar chunks)
        |
        v
    Augment prompt (Combine query with retrived context)
        |
        v
    LLM generates response (Grounded, context-aware answer)

```