# chunking strategy

Token/character-based chunking with overlap.

Chunk size: 1000 characters
Overlap:    200 characters


Structure of chunk :

Now 
```
{
    "page_number": 4,
    "chunk_index": 12,
    "text": "...",
}
```
Later 
```
{
    "document_id": "...",
    "document_name": "leave_policy.pdf",
    "page_number": 4,
    "chunk_index": 12,
    "text": "...",
    "embedding": [...]
}
```

Look at the Quality of the chunks.

ask yourself :

1. Is each chunk understandable by itself?
2. Are sentences being cut in the middle?

chunking strategy :

1. fixed-sized chunking
2. sentence-based chunking
3. paragraph-based chunking
4. section-aware chunking
5. recursive chunking
6. semantic chunking
7. parent-child chunking
8. document-structure-aware chunking