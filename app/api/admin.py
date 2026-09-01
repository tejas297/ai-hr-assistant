import os
import shutil
import tempfile
import zipfile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.schemas import LoginRequest, LoginResponse, UploadError, UploadResponse
from app.auth import authenticate_admin, create_access_token, get_current_admin
from app.database.connection import SessionLocal
from app.ingestion.ingestion_service import ingest_pdf

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/login", response_model=LoginResponse)
def admin_login(payload: LoginRequest):
    if not authenticate_admin(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(payload.username)
    return LoginResponse(
        access_token=token,
        token_type="bearer",
        username=payload.username,
        message="Login successful",
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_upload_file(upload_file: UploadFile, temp_dir: str) -> str:
    """Save an uploaded file to a temporary directory."""
    file_path = os.path.join(temp_dir, upload_file.filename)
    with open(file_path, "wb") as f:
        f.write(upload_file.file.read())
    return file_path


def extract_zip_file(zip_path: str, extract_dir: str) -> list[str]:
    """Extract a zip file and return paths to PDF files."""
    pdf_paths = []
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
        
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                if file.lower().endswith(".pdf"):
                    pdf_paths.append(os.path.join(root, file))
    except zipfile.BadZipFile as e:
        raise HTTPException(status_code=400, detail=f"Invalid zip file: {str(e)}")
    
    return pdf_paths


@router.post("/upload-document")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    """
    Upload a single PDF document.
    
    The document will be chunked, embedded, and stored in the database.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        file_path = save_upload_file(file, temp_dir)
        
        chunk_count = ingest_pdf(
            db=db,
            file_path=file_path,
            document_name=file.filename,
        )
        
        return UploadResponse(
            success=True,
            message=f"Successfully ingested {file.filename}",
            document_name=file.filename,
            chunks_created=chunk_count,
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to ingest document: {str(e)}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@router.post("/upload-documents")
def upload_documents(
    files: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    """
    Upload multiple PDF documents at once.
    
    Each document will be chunked, embedded, and stored separately.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    temp_dir = tempfile.mkdtemp()
    results = []
    errors = []
    
    try:
        for file in files:
            if not file.filename.lower().endswith(".pdf"):
                errors.append(
                    UploadError(
                        filename=file.filename,
                        error="File must be a PDF",
                    )
                )
                continue
            
            try:
                file_path = save_upload_file(file, temp_dir)
                
                chunk_count = ingest_pdf(
                    db=db,
                    file_path=file_path,
                    document_name=file.filename,
                )
                
                results.append(
                    UploadResponse(
                        success=True,
                        message=f"Successfully ingested {file.filename}",
                        document_name=file.filename,
                        chunks_created=chunk_count,
                    )
                )
            except Exception as e:
                db.rollback()
                errors.append(
                    UploadError(
                        filename=file.filename,
                        error=str(e),
                    )
                )
        
        if not results and errors:
            raise HTTPException(status_code=400, detail=f"All files failed: {errors}")
        
        return {
            "success": len(results) > 0,
            "uploaded": results,
            "failed": errors,
            "summary": f"Uploaded {len(results)} document(s), {len(errors)} failed.",
        }
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@router.post("/upload-zip")
def upload_zip(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    """
    Upload a zip file containing PDF documents.
    
    All PDF files in the zip will be extracted, chunked, embedded, and stored.
    """
    if not file.filename.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="File must be a zip archive")
    
    temp_dir = tempfile.mkdtemp()
    extract_dir = os.path.join(temp_dir, "extracted")
    os.makedirs(extract_dir)
    
    results = []
    errors = []
    
    try:
        zip_path = save_upload_file(file, temp_dir)
        pdf_paths = extract_zip_file(zip_path, extract_dir)
        
        if not pdf_paths:
            raise HTTPException(status_code=400, detail="No PDF files found in zip archive")
        
        for pdf_path in pdf_paths:
            try:
                document_name = os.path.basename(pdf_path)
                
                chunk_count = ingest_pdf(
                    db=db,
                    file_path=pdf_path,
                    document_name=document_name,
                )
                
                results.append(
                    UploadResponse(
                        success=True,
                        message=f"Successfully ingested {document_name}",
                        document_name=document_name,
                        chunks_created=chunk_count,
                    )
                )
            except Exception as e:
                db.rollback()
                errors.append(
                    UploadError(
                        filename=os.path.basename(pdf_path),
                        error=str(e),
                    )
                )
        
        if not results and errors:
            raise HTTPException(status_code=400, detail=f"No files processed: {errors}")
        
        return {
            "success": len(results) > 0,
            "uploaded": results,
            "failed": errors,
            "summary": f"Processed {len(results)} document(s) from zip, {len(errors)} failed.",
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to process zip: {str(e)}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
