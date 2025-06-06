# Importing necessary modules
from sqlalchemy.orm import Session
from api.database.models.user import User  # Importing the User model
from api.database.schemas.user import UserCreate, UserUpdate  # Importing schemas for user data validation
from datetime import datetime  # For handling timestamps
from api.security import hash_password  # For hashing passwords before storing

# Function to create a new user in the database
def create_user(db: Session, user: UserCreate):
    """
    Creates a new user with hashed password and stores it in the database.
    
    :param db: Database session.
    :param user: User data from the request.
    :return: The newly created user object.
    """
    # Create a new User instance with data from the request
    db_user = User(
        name=user.name,  # User's full name
        email=user.email,  # User's email
        password=hash_password(user.password),  # Hash the password before storing
        mob_number=user.mob_number,  # User's mobile number
        role="customer",  # Default role for a new user is 'customer'
        created_at=datetime.utcnow(),  # Timestamp of user creation (current time in UTC)
        updated_at=None  # No update timestamp initially
    )
    
    # Add the new user to the database session
    db.add(db_user)
    
    # Commit the transaction to save changes to the database
    db.commit()
    
    # Refresh the user instance to retrieve the latest data from the database
    db.refresh(db_user)
    
    # Return the newly created user object
    return db_user


# Function to retrieve a user by email
def get_user_by_email(db: Session, email: str):
    """
    Fetches a user from the database using their email.
    
    :param db: Database session.
    :param email: User's email address.
    :return: User object if found, else None.
    """
    # Query the database for a user with the given email
    return db.query(User).filter(User.email == email).first()


# Function to retrieve a user by mobile number
def get_user_by_mobile(db: Session, mob_number: str):
    """
    Fetches a user from the database using their mobile number.
    
    :param db: Database session.
    :param mob_number: User's mobile number.
    :return: User object if found, else None.
    """
    # Query the database for a user with the given mobile number
    return db.query(User).filter(User.mob_number == mob_number).first()


# Function to retrieve a user by ID
def get_user_by_id(db: Session, user_id: int):
    """
    Fetches a user from the database using their unique ID.
    
    :param db: Database session.
    :param user_id: User's unique identifier.
    :return: User object if found, else None.
    """
    # Query the database for a user with the given ID
    return db.query(User).filter(User.id == user_id).first()


# Function to retrieve all users or a specific user by ID
def get_users(db: Session, user_id: int | None = None):
    """
    Fetches all users or a specific user by their ID.
    
    :param db: Database session.
    :param user_id: Optional user ID to fetch a single user. If None, fetches all users.
    :return: List of users or a single user object if user_id is provided.
    """
    if user_id:
        # Query for a user with the given ID
        return db.query(User).filter(User.id == user_id).first()
    
    # Query for all users if no user_id is provided
    return db.query(User).all()


# Function to update an existing user
def update_user(db: Session, user_id: int, user: UserUpdate):
    """
    Updates an existing user with new data.
    
    :param db: Database session.
    :param user_id: User's unique identifier.
    :param user: User data to update.
    :return: Updated user object if successful, else None.
    """
    # Fetch the user from the database by their ID
    db_user = db.query(User).filter(User.id == user_id).first()
    
    # If the user doesn't exist, return None
    if not db_user:
        return None

    # Iterate over the fields of the UserUpdate object and update the corresponding user data
    for key, value in user.dict(exclude_unset=True).items():
        if key == "password":
            # If the field is 'password', hash the new value before storing it
            value = hash_password(value)
        setattr(db_user, key, value)  # Set the new value on the user object
    
    # Set the updated timestamp to the current time in UTC
    db_user.updated_at = datetime.utcnow()
    
    # Commit the changes to the database
    db.commit()
    
    # Refresh the user instance with the latest data from the database
    db.refresh(db_user)
    
    # Return the updated user object
    return db_user


# Function to delete a user from the database
def delete_user(db: Session, user_id: int):
    """
    Deletes a user from the database.
    
    :param db: Database session.
    :param user_id: User's unique identifier.
    :return: Deleted user object if found, else None.
    """
    # Fetch the user from the database by their ID
    db_user = db.query(User).filter(User.id == user_id).first()
    
    # If the user exists, delete them from the database
    if db_user:
        db.delete(db_user)
        db.commit()  # Commit the transaction to remove the user
    return db_user  # Return the deleted user object (or None if not found)
