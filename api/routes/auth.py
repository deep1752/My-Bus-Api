from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.connection import get_db
from api.database.schemas.user import UserCreate, UserLogin, UserResponse
from api.crud.user import create_user, get_user_by_email, get_user_by_mobile
from api.security import verify_password
from fastapi.security import OAuth2PasswordBearer
from api.token import create_access_token

# ----------------------------------------------------------------------------
# Create a new FastAPI router to handle user authentication (register/login)
# ----------------------------------------------------------------------------
router = APIRouter()

# Define the OAuth2 scheme using the password grant flow
# This is used to extract the token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ----------------------------------------------------------------------------
# Route: POST /register
# Description: Register a new user account
# ----------------------------------------------------------------------------
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user in the system.

    Steps:
    - Check if the email is already registered.
    - Check if the mobile number is already registered.
    - If both are unique, create the new user in the database.

    Parameters:
    - user: Request body with fields like name, email, password, mobile number, etc.
    - db: Database session dependency

    Returns:
    - A UserResponse object excluding sensitive info like password
    """

    # Check if the email already exists in the system
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if the mobile number already exists in the system
    existing_mobile = get_user_by_mobile(db, user.mob_number)
    if existing_mobile:
        raise HTTPException(status_code=400, detail="Mobile number already registered")

    # All good, proceed to create the user and return the created user
    return create_user(db, user)


# ----------------------------------------------------------------------------
# Route: POST /login
# Description: Authenticate a user and return a JWT token
# ----------------------------------------------------------------------------
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT access token if credentials are valid.

    Steps:
    - Find user by email.
    - Verify the password.
    - If valid, create and return an access token.

    Parameters:
    - user: Request body containing email and password
    - db: Database session dependency

    Returns:
    - A dictionary with the access token and token type
    """

    # Fetch user record by email
    db_user = get_user_by_email(db, user.email)

    # If user not found or password does not match, raise an error
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    # Generate a JWT access token with user email as the subject
    access_token = create_access_token(data={"sub": db_user.email})

    # Return the token and its type to the client
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }