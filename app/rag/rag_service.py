
from sqlalchemy.orm import Session

from app.llm.client import LLMClient
from app.rag.context_builder import build_context
from app.rag.prompt_builder import build_prompt
from app.rag.schemas import RAGResponse, Source
from app.retrieval.search import search_similar_chunks



"""
The RAG service doesn't know how anything works internally.

It just orchestrates:

    search_similar_chunks()
            ↓
    build_context()
            ↓
    build_prompt()
            ↓
    llm.generate()
"""

class RAGService:

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def answer(
        self,
        db: Session,
        question: str,
    ) -> RAGResponse:

        results = search_similar_chunks(
            db=db,
            query=question,
            top_k=5,
        )

        if not results:
            return RAGResponse(
                answer=(
                    "I could not find this information "
                    "in the available HR policies."
                ),
                sources=[],
            )

        context = build_context(results)

        prompt = build_prompt(
            context=context,
            question=question,
        )

        answer = self.llm.generate(prompt)

        sources = []

        seen = set()

        for result in results:
            source_key = (
                result.chunk.document_name,
                result.chunk.page_number,
            )

            if source_key in seen:
                continue

            seen.add(source_key)

            sources.append(
                Source(
                    document_name=result.chunk.document_name,
                    page_number=result.chunk.page_number,
                )
            )

        return RAGResponse(
            answer=answer,
            sources=sources,
        )