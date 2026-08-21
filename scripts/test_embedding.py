from app.ingestion.embedding import generate_embedding


text = "Employees are entitled to 25 paid leaves per year."

embedding = generate_embedding(text)

print("Embedding generated successfully")
print("Dimension:", len(embedding))
print("First 10 values:", embedding)