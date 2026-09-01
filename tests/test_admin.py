import io
import zipfile

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_admin_token():
    login_response = client.post(
        "/admin/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert login_response.status_code == 200
    return login_response.json()["access_token"]


def test_admin_login_success():
    response = client.post(
        "/admin/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_upload_document_rejects_non_pdf():
    """Test that non-PDF files are rejected."""
    token = get_admin_token()
    response = client.post(
        "/admin/upload-document",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.txt", io.BytesIO(b"not a pdf"), "text/plain")},
    )
    assert response.status_code == 400
    assert "File must be a PDF" in response.text


def test_upload_documents_rejects_non_pdf():
    """Test that non-PDF files are rejected in batch upload."""
    token = get_admin_token()
    response = client.post(
        "/admin/upload-documents",
        headers={"Authorization": f"Bearer {token}"},
        files=[
            ("files", ("test1.txt", io.BytesIO(b"not pdf 1"), "text/plain")),
            ("files", ("test2.txt", io.BytesIO(b"not pdf 2"), "text/plain")),
        ],
    )
    assert response.status_code == 400


def test_upload_zip_rejects_non_zip():
    """Test that non-zip files are rejected."""
    token = get_admin_token()
    response = client.post(
        "/admin/upload-zip",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.pdf", io.BytesIO(b"not a pdf"), "application/pdf")},
    )
    assert response.status_code == 400
    assert "File must be a zip archive" in response.text


def test_upload_zip_rejects_zip_without_pdfs():
    """Test that zip files without PDFs are rejected."""
    token = get_admin_token()
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        zip_file.writestr("test.txt", "not a pdf")
    zip_buffer.seek(0)

    response = client.post(
        "/admin/upload-zip",
        headers={"Authorization": f"Bearer {token}"},
        files={"file": ("test.zip", zip_buffer, "application/zip")},
    )
    assert response.status_code == 400
    assert "No PDF files found" in response.text


def test_upload_documents_with_no_files():
    """Test that upload-documents requires at least one file."""
    token = get_admin_token()
    response = client.post(
        "/admin/upload-documents",
        headers={"Authorization": f"Bearer {token}"},
        files=[],
    )
    assert response.status_code == 422
