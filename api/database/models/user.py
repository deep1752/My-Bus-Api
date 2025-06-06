
from sqlalchemy import Column, Integer, String, DateTime, func
from api.database.connection import Base  # Importing the base class for the model 

# Defining the User model which will represent the "users" table in the database
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    """
    email: User's email address.
    - String type with a maximum length of 255 characters.
    - 'unique=True' ensures that no two users can have the same email address.
    - 'index=True' allows the email to be indexed for faster search queries.
    - 'nullable=False' means this field must be provided.
    """
    password = Column(String(255), nullable=False)
    mob_number = Column(String(15), unique=True, nullable=False)
    role = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    """
    created_at: The timestamp when the user was created.
    - 'DateTime' type stores date and time information.
    - 'default=func.now()' automatically sets this field to the current date and time when the user is created.
    """
    
    updated_at = Column(DateTime, nullable=True)
