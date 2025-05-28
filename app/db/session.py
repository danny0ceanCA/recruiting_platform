import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Print to confirm the DB URL in use
print("Using database URL:", DATABASE_URL)

# Create engine with SQLite-specific arguments if needed
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Session factory (models use Base from app.db.base_class)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
