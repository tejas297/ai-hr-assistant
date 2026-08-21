from app.database.connection import SessionLocal
from app.retrieval.search import search_similar_chunks
from app.rag.context_builder import build_context
from app.rag.prompt_builder import build_prompt


QUERY = "What is the approval process for IT assets?"


def main():
    db = SessionLocal()

    try:
        results = search_similar_chunks(
            db=db,
            query=QUERY,
            top_k=5,
        )

        context = build_context(results)

        prompt = build_prompt(
            context=context,
            question=QUERY,
        )

        print("===== PROMPT =====")
        print(prompt)
        print("==================")

    finally:
        db.close()


if __name__ == "__main__":
    main()