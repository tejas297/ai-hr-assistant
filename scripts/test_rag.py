from dotenv import load_dotenv

from app.database.connection import SessionLocal
from app.llm.groq_client import GroqClient
from app.rag.rag_service import RAGService


load_dotenv()


QUESTION = "What is the approval process for IT assets?" # test - 1
# QUESTION = "What is the company's maternity leave policy?" # test - 2

def main():

    db = SessionLocal()

    try:
        llm = GroqClient()

        rag = RAGService(
            llm=llm,
        )

        response = rag.answer(
            db=db,
            question=QUESTION,
        )

        print("===== QUESTION =====")
        print(QUESTION)

        print("\n===== ANSWER =====")
        print(response.answer)

        print("\n===== SOURCES =====")

        for source in response.sources:
            print(
                f"- {source.document_name}, "
                f"Page {source.page_number}"
            )

    finally:
        db.close()


if __name__ == "__main__":
    main()



    """
    The below flow will be executed when the script is run:

    "What is the approval process for IT assets?"
                │
                ↓
       Sentence Transformer
                │
                ↓
             384D
                │
                ↓
        PostgreSQL pgvector
                │
                ↓
          distance ≤ 0.5
                │
                ↓
         SearchResult[]
                │
                ↓
        Context Builder
                │
                ↓
          Context String
                │
                ↓
        Prompt Builder
                │
                ↓
             Prompt
                │
                ↓
             Groq LLM
                │
                ↓
          Generated Answer
    """