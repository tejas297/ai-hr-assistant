from app.llm.groq_client import GroqClient
from app.rag.rag_service import RAGService


llm_client = GroqClient()
rag_service = RAGService(llm=llm_client)


def get_rag_service() -> RAGService:
    return rag_service