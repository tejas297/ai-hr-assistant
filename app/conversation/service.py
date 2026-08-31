from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Conversation, Message


class ConversationService:

    def get_or_create_conversation(
        self,
        db: Session,
        session_id: str,
    ) -> Conversation:

        statement = select(Conversation).where(
            Conversation.session_id == session_id
        )

        conversation = db.scalar(statement)

        if conversation is not None:
            return conversation

        conversation = Conversation(
            session_id=session_id,
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    def add_message(
        self,
        db: Session,
        conversation_id: int,
        role: str,
        content: str,
    ) -> Message:

        if role not in {"user", "assistant"}:
            raise ValueError(
                "role must be either 'user' or 'assistant'"
            )

        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    def get_messages(
        self,
        db: Session,
        conversation_id: int,
    ) -> list[Message]:

        statement = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id
            )
            .order_by(
                Message.created_at,
                Message.id,
            )
        )

        return list(db.scalars(statement).all())

    def get_recent_messages(
        self,
        db: Session,
        conversation_id: int,
        limit: int = 10,
    ) -> list[Message]:

        statement = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id
            )
            .order_by(
                Message.created_at.desc(),
                Message.id.desc(),
            )
            .limit(limit)
        )

        messages = list(db.scalars(statement).all())

        messages.reverse()

        return messages