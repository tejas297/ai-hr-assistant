from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas import ChatRequest, ChatResponse
from app.database.connection import SessionLocal
from app.llm.groq_client import GroqClient
from app.rag.rag_service import RAGService


router = APIRouter()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    llm = GroqClient()

    rag_service = RAGService(
        llm=llm,
    )

    result = rag_service.answer(
        db=db,
        question=request.question,
    )

    return ChatResponse(
        answer=result.answer,
        sources=[
            {
                "document_name": source.document_name,
                "page_number": source.page_number,
            }
            for source in result.sources
        ],
    )