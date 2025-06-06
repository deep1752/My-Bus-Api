
from sqlalchemy import create_engine  # For creating a database engine
from sqlalchemy.ext.declarative import declarative_base  # For defining the base class for models
from sqlalchemy.orm import sessionmaker  # For creating database sessions
from api.config import DATABASE_URL  # Import the database URL from the configuration file

# Create the database engine using the DATABASE_URL from config
# `check_same_thread` argument is needed for SQLite, but ignored for other databases.
engine = create_engine(
    DATABASE_URL,  # Database URL (e.g., 'postgresql://user:password@localhost/dbname' or 'sqlite:///./test.db')
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}  # SQLite-specific argument
)

# Create a sessionmaker object to manage database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base class for SQLAlchemy models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    """
    Dependency to get a database session.
    
    This function is used as a dependency for FastAPI routes to provide a 
    database session to the API endpoints.
    
    :yield: A database session object.
    """
    db = SessionLocal()  # Create a new session using the sessionmaker
    try:
        yield db  # Yield the session to be used by the endpoint
    finally:
        db.close()  # Close the session after the request is processed
