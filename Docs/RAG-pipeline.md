
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

## threshold implimentation give us an important RAG safety machanism 

```
User:
"What is the maternity leave policy?"

             ↓

Embedding
             ↓

Vector Search
             ↓

Best distance = 0.7301
             ↓

0.7301 > 0.5
             ↓

NO RELEVANT HR CONTEXT
             ↓

Don't call LLM with unrelated documents
             ↓
"I couldn't find this information
 in the available HR policies."
```