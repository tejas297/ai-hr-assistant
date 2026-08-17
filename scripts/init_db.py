from app.database.connection import engine
from app.database.models import Base

# Create the database tables based on the defined models
Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")