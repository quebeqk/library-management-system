from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables from .env file
load_dotenv()

# Read database config from .env file
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Encoding the password to handle special characters
encoded_password = quote_plus(DB_PASSWORD)

# SQLAlchemy Database URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}"

# Create SQLAlchemy Engine
engine = create_engine(DATABASE_URL, echo=True)

# Create Session Factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Function to initialize database tables
def init_db():
    from .models import User, Book, BorrowRequest, BorrowHistory
    Base.metadata.create_all(bind=engine) # Create tables if they don't exist
    print("Tables created successfully")

# Dependency function to get a database session
def get_db():
    db = SessionLocal()  # Create a new session
    try:
        yield db  # Yield session (used for dependency injection)
    finally:
        db.close() # Close session when done