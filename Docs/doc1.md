# AI HR Assistant

## problem
     HR policies are often stored as PDFs/DOCX files. Employees have to manually search through them or ask HR.
     Our system will allow employees to ask natural-language questions and get answers grounded in the organization's HR documents.

## Core flow
```
 HR Admin
   │
   │ Upload HR Policy
   ▼
┌─────────────────┐
│ Document        │
│ Processing      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Chunking        │
│ + Metadata      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Embeddings      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PostgreSQL      │
│ + pgvector      │
└─────────────────┘


Employee
   │
   │ "How many paid leaves?"
   ▼
┌─────────────────┐
│ Query Processing│
└────────┬────────┘
         ▼
┌─────────────────┐
│ Vector Search   │
└────────┬────────┘
         ▼
┌─────────────────┐
│ Relevant Policy │
│ Chunks          │
└────────┬────────┘
         ▼
┌─────────────────┐
│ LLM             │
│ Answer          │
└────────┬────────┘
         ▼
┌─────────────────────────┐
│ Answer + Sources        │
└─────────────────────────┘
 ```


## MVP Requirements

    1. HR Admin

    Admin should be able to:

        Upload HR policy documents
        View uploaded documents
        Delete documents
        Re-upload updated policies
        See document processing status

        Supported initially:
            PDF
            DOCX
            TXT

    2. Employee

    Employee should be able to:

        Ask questions
        Receive natural-language answers
        See supporting document
        See page/section where possible
        Ask follow-up questions
        View conversation history

    3. AI behavior

    The assistant must:

    Answer from HR documents only.

    For example:

        "How many paid leaves do employees get?"

        If the policy says 24:

        Employees are entitled to 24 paid leaves per year.

        With:

        Source:
        Employee Leave Policy
        Page: 4
        Section: Annual Leave

        If the information isn't available:

        I couldn't find this information in the available HR policies. Please contact HR for clarification.

        The assistant must not invent HR policies.


    RAG Architecture :
        User Question
            ↓
        Embedding
            ↓
        Vector Search
            ↓
        Relevant HR Policy
            ↓
        LLM
            ↓
        Grounded Answer

## Functional Requirements

```
FR-01 — Document Upload

Admin can upload an HR document.

FR-02 — Document Processing

System extracts text from the document.

FR-03 — Chunking

System divides documents into meaningful chunks.

FR-04 — Embedding

System generates embeddings for each chunk.

FR-05 — Vector Storage

System stores embeddings in PostgreSQL/pgvector.

FR-06 — Semantic Search

System finds relevant chunks based on the employee's question.

FR-07 — Answer Generation

LLM generates an answer using retrieved chunks.

FR-08 — Source Citation

Answer contains document and page/section information where available.

FR-09 — No-Answer Handling

If relevant information cannot be found, system must not fabricate an answer.

FR-10 — Conversation

Employee can ask follow-up questions.
```

## Non Fucntional Requirements

```
Security

HR documents can contain sensitive information.

Therefore:

Authentication
Authorization
Document access control
Audit logging

must eventually be included.

Performance

Target for MVP:

Question → Answer


< 5 seconds

We can optimize this later.

Availability

The system should continue working if one document fails during ingestion.

Example:

10 documents uploaded


9 → SUCCESS
1 → FAILED

The entire ingestion job should not fail.

Scalability

Architecture should eventually support:

10 documents
       ↓
100 documents
       ↓
10,000 documents

without redesigning the entire application.
```

## MVP

```
    Document Upload
        ↓
    Text Extraction
        ↓
    Chunking
        ↓
    Embeddings
        ↓
    pgvector
        ↓
    Semantic Search
        ↓
    LLM
        ↓
    Answer + Source
```

## Later

```
    Authentication
    RBAC
    Document versioning
    Conversation memory
    Feedback
    Evaluation
    Analytics
    Audit logs
    PII detection
    Prompt injection protection
    Multi-tenant architecture
    Department-specific policies
```

```
conversations
-------------------------
id
session_id
created_at
updated_at


messages
-------------------------
id
conversation_id
role
content
created_at

```