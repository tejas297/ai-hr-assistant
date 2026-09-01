# Admin API Endpoints

The admin API provides endpoints for managing document uploads and ingestion into the HR assistant system.

## Base URL
All admin endpoints are prefixed with `/admin`

## Endpoints

### 1. Upload Single Document
**Endpoint:** `POST /admin/upload-document`

Upload a single PDF document that will be chunked, embedded, and stored in the database.

**Parameters:**
- `file` (form-data, required): PDF file to upload

**Response:**
```json
{
  "success": true,
  "message": "Successfully ingested document_name.pdf",
  "document_name": "document_name.pdf",
  "chunks_created": 45
}
```

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/admin/upload-document" \
  -F "file=@/path/to/policy.pdf"
```

**Example with Python:**
```python
import requests

with open('policy.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/admin/upload-document',
        files=files
    )
print(response.json())
```

---

### 2. Upload Multiple Documents
**Endpoint:** `POST /admin/upload-documents`

Upload multiple PDF documents at once. Each will be processed independently.

**Parameters:**
- `files` (form-data, required): Multiple PDF files to upload

**Response:**
```json
{
  "success": true,
  "uploaded": [
    {
      "success": true,
      "message": "Successfully ingested policy1.pdf",
      "document_name": "policy1.pdf",
      "chunks_created": 45
    },
    {
      "success": true,
      "message": "Successfully ingested policy2.pdf",
      "document_name": "policy2.pdf",
      "chunks_created": 38
    }
  ],
  "failed": [
    {
      "filename": "invalid.txt",
      "error": "File must be a PDF"
    }
  ],
  "summary": "Uploaded 2 document(s), 1 failed."
}
```

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/admin/upload-documents" \
  -F "files=@/path/to/policy1.pdf" \
  -F "files=@/path/to/policy2.pdf" \
  -F "files=@/path/to/policy3.pdf"
```

**Example with Python:**
```python
import requests

files = [
    ('files', open('policy1.pdf', 'rb')),
    ('files', open('policy2.pdf', 'rb')),
    ('files', open('policy3.pdf', 'rb'))
]
response = requests.post(
    'http://localhost:8000/admin/upload-documents',
    files=files
)
print(response.json())
```

---

### 3. Upload Zip Archive
**Endpoint:** `POST /admin/upload-zip`

Upload a zip file containing multiple PDF documents. All PDFs will be extracted and processed.

**Parameters:**
- `file` (form-data, required): Zip archive containing PDF files

**Response:**
```json
{
  "success": true,
  "uploaded": [
    {
      "success": true,
      "message": "Successfully ingested policy1.pdf",
      "document_name": "policy1.pdf",
      "chunks_created": 45
    },
    {
      "success": true,
      "message": "Successfully ingested policy2.pdf",
      "document_name": "policy2.pdf",
      "chunks_created": 38
    }
  ],
  "failed": [],
  "summary": "Processed 2 document(s) from zip, 0 failed."
}
```

**Example with cURL:**
```bash
curl -X POST "http://localhost:8000/admin/upload-zip" \
  -F "file=@/path/to/policies.zip"
```

**Example with Python:**
```python
import requests

with open('policies.zip', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:8000/admin/upload-zip',
        files=files
    )
print(response.json())
```

**Zip Structure Example:**
```
policies.zip
├── Leave_Policy.pdf
├── Work_From_Home_Policy.pdf
├── Travel_Policy.pdf
└── subfolder/
    └── Benefits_Policy.pdf
```

---

## Error Responses

### 400 Bad Request
- File is not a PDF (for single/multiple upload)
- File is not a zip archive (for zip upload)
- No PDF files found in zip archive
- Invalid zip file format

### 422 Unprocessable Content
- No files provided to upload-documents endpoint
- Missing required file parameter

### 500 Internal Server Error
- Database operation failed
- PDF extraction error
- Embedding generation failed

---

## Processing Details

Each uploaded PDF document is processed through the following steps:

1. **Text Extraction**: Extract text from all pages of the PDF
2. **Chunking**: Split text into semantic chunks with page metadata
3. **Embedding Generation**: Generate vector embeddings using sentence transformers
4. **Storage**: Store chunks and embeddings in PostgreSQL with pgvector

The chunks are then available for semantic search through the `/chat` endpoint.

---

## Limits and Constraints

- File size: No hard limit, but practical limit depends on server memory
- PDF format: Only standard PDF files are supported
- Zip nesting: Supports nested directories within zip files
- Document name: Taken from filename, must be unique
- Chunks: All chunks from a document reference the original document name

---

## Testing

Run the admin tests with:
```bash
pytest tests/test_admin.py -v
```

All tests validate:
- File type validation
- Error handling
- Proper error messages
- Response format correctness
