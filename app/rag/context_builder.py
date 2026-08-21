from app.retrieval.schemas import SearchResult


def build_context(results: list[SearchResult]) -> str:
    if not results:
        return ""

    context_parts = []

    for result in results:
        chunk = result.chunk

        context_parts.append(
            f"[Source: {chunk.document_name}, Page {chunk.page_number}]\n"
            f"{chunk.content}"
        )

    return "\n\n".join(context_parts)