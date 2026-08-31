from app.conversation.service import ConversationService
from app.conversation.question_resolver import QuestionResolver
from app.llm.groq_client import GroqClient
from app.rag.rag_service import RAGService


_conversation_service = ConversationService()


def get_rag_service() -> RAGService:

    llm = GroqClient()
    question_resolver = QuestionResolver(llm=llm)

    return RAGService(
        llm=llm,
        question_resolver=question_resolver,
    )


def get_conversation_service() -> ConversationService:

    return _conversation_service