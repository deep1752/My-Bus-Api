from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database.schemas.user import UserResponse, UserUpdate
from api.token import get_current_user
from api.crud import user as user_crud
from api.database.connection import get_db

# Create an instance of the APIRouter to define route group for users
router = APIRouter()

# ----------------------------------------------------------
# Route: GET /profile
# Description: Returns the profile of the current logged-in user
# Auth Required: Yes (Depends on get_current_user)
# ----------------------------------------------------------
@router.get("/profile", response_model=UserResponse)
def get_profile(current_user: UserResponse = Depends(get_current_user)):
    """
    Fetch the profile details of the currently authenticated user.
    Uses token-based authentication to get user info.
    """
    return current_user


# ----------------------------------------------------------
# Route: GET /users
# Description: Returns all users or a specific user by ID
# Query Param: user_id (optional)
# ----------------------------------------------------------
@router.get("/users", response_model=list[UserResponse])
def read_users(
    user_id: int = None, 
    db: Session = Depends(get_db)
):
    """
    Fetch all users from the database or a single user if 'user_id' is provided.
    Returns a list of UserResponse models.
    
    Args:
        user_id (int, optional): ID of the specific user to fetch.
        db (Session): SQLAlchemy DB session dependency.
    
    Raises:
        HTTPException: If user_id is provided and no user is found.
    
    Returns:
        list[UserResponse]: List of users or a single user inside a list.
    """
    result = user_crud.get_users(db, user_id)
    
    # If user_id is provided but no user found, raise 404
    if user_id and not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # If result is a list, return it, otherwise wrap single result in a list
    return result if isinstance(result, list) else [result]


# ----------------------------------------------------------
# Route: PUT /update/{user_id}
# Description: Updates user details based on the given user_id
# ----------------------------------------------------------
@router.put("/update/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, 
    user: UserUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update a user’s information in the database using their user_id.
    
    Args:
        user_id (int): The ID of the user to update.
        user (UserUpdate): Pydantic model containing updated fields.
        db (Session): SQLAlchemy DB session.
    
    Raises:
        HTTPException: If the user with given ID does not exist.
    
    Returns:
        UserResponse: The updated user object.
    """
    updated_user = user_crud.update_user(db, user_id, user)
    
    # Raise 404 if user doesn't exist
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user


# ----------------------------------------------------------
# Route: DELETE /delete/{user_id}
# Description: Deletes the user with the given user_id
# ----------------------------------------------------------
@router.delete("/delete/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db)
):
    """
    Delete a user from the database using their user_id.
    
    Args:
        user_id (int): ID of the user to delete.
        db (Session): SQLAlchemy DB session.
    
    Raises:
        HTTPException: If the user is not found.
    
    Returns:
        UserResponse: The deleted user’s data.
    """
    deleted_user = user_crud.delete_user(db, user_id)
    
    # Raise 404 if no such user found
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return deleted_user
