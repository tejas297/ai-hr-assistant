from app.database.connection import SessionLocal
from app.retrieval.search import search_similar_chunks


QUERY = "who will approve the asset approval policy?"
# QUERY = "What is the approval process for IT assets?"  # test -1
# QUERY = "What is the company's maternity leave policy?" # test -2 
def main():

    db = SessionLocal()

    try:

        results = search_similar_chunks(
            db=db,
            query=QUERY,
            top_k=5,
        )

        for result in results:
                chunk = result.chunk
                distance = result.distance
                print(
                     f"page={chunk.page_number}, "
                     f"chunk={chunk.chunk_index}, "
                     f"distance={distance:.4f}"
         )

                # print(chunk.content)
                print("-" * 80)
                    
    finally:

        db.close()


if __name__ == "__main__":
    main() 