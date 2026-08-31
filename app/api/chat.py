from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_conversation_service,
    get_rag_service,
)
from app.api.schemas import ChatRequest, ChatResponse
from app.conversation.history import build_history
from app.conversation.service import ConversationService
from app.database.connection import SessionLocal
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
    rag_service: RAGService = Depends(get_rag_service),
    conversation_service: ConversationService = Depends(
        get_conversation_service
    ),
):
    conversation = (
        conversation_service.get_or_create_conversation(
            db=db,
            session_id=request.session_id,
        )
    )

    history_messages = (
        conversation_service.get_recent_messages(
            db=db,
            conversation_id=conversation.id,
            limit=10,
        )
    )

    history = build_history(history_messages)

    conversation_service.add_message(
        db=db,
        conversation_id=conversation.id,
        role="user",
        content=request.question,
    )


    try:
         result = rag_service.answer(
        db=db,
        question=request.question,
        history=history,
    )
    except Exception:
        db.rollback()
        raise

    conversation_service.add_message(
        db=db,
        conversation_id=conversation.id,
        role="assistant",
        content=result.answer,
    )

    return ChatResponse(
        answer=result.answer,
        reasoning=result.reasoning,
        sources=[
            {
                "document_name": source.document_name,
                "page_number": source.page_number,
            }
            for source in result.sources
        ],
    )