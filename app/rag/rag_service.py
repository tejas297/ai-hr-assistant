import re

from sqlalchemy.orm import Session

from app.conversation.question_resolver import QuestionResolver
from app.llm.client import LLMClient
from app.rag.context_builder import build_context
from app.rag.prompt_builder import build_prompt
from app.rag.schemas import RAGResponse, Source
from app.retrieval.search import search_similar_chunks


def split_reasoning(response: str) -> tuple[str, str]:
    """Separate optional model reasoning from the user-facing answer."""
    if not response:
        return "", ""

    raw_response = response.strip()

    reasoning_blocks = re.findall(
        r"<(?:think|thinking)\b[^>]*>(.*?)</(?:think|thinking)\s*>",
        raw_response,
        flags=re.IGNORECASE | re.DOTALL,
    )

    answer = re.sub(
        r"\s*<(?:think|thinking)\b[^>]*>.*?</(?:think|thinking)\s*>\s*",
        "\n",
        raw_response,
        flags=re.IGNORECASE | re.DOTALL,
    ).strip()

    if reasoning_blocks:
        return answer, "\n\n".join(block.strip() for block in reasoning_blocks)

    reasoning_prefix = re.compile(
        r"(?is)^(?:here's\s+)?(?:a\s+)?(?:thinking process|analysis|reasoning)\s*[:\-]?\s*"
    )
    parts = re.split(r"\n\s*\n+", raw_response, maxsplit=1)

    if len(parts) == 2:
        first_part = parts[0].strip()
        second_part = parts[1].strip()

        if reasoning_prefix.match(first_part):
            reasoning_text = reasoning_prefix.sub("", first_part).strip()
            if reasoning_text:
                return second_part, reasoning_text

    return answer or raw_response, "\n\n".join(block.strip() for block in reasoning_blocks)


class RAGService:

    def __init__(
        self,
        llm: LLMClient,
        question_resolver: QuestionResolver | None = None,
    ):
        self.llm = llm
        self.question_resolver = question_resolver

    def answer(
        self,
        db: Session,
        question: str,
        history: str = "No previous conversation.",
    ) -> RAGResponse:

        search_question = question

        if self.question_resolver is not None:
            search_question = self.question_resolver.resolve(
                question=question,
                history=history,
            )

        results = search_similar_chunks(
            db=db,
            query=search_question,
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
            question=search_question,
        )

        answer, reasoning = split_reasoning(self.llm.generate(prompt))

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
            reasoning=reasoning,
        )