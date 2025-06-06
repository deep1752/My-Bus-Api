
from pydantic import BaseModel, EmailStr  # BaseModel from Pydantic helps with data validation, EmailStr for email validation
from datetime import datetime  # Importing datetime for date/time fields
from typing import Optional  # Importing Optional for fields that may or may not be provided

# ----------------------------------------------------------------------------
# User Creation Model - Used to validate the data sent when creating a user
# ----------------------------------------------------------------------------
class UserCreate(BaseModel):
    """
    Pydantic model to validate input data for creating a new user.
    It is used for requests when registering a new user.
    """
    
    name: str  
    email: EmailStr  
    password: str  
    mob_number: str  

    
    # role: str  
    # created_at: datetime  
    # updated_at: datetime  

# ----------------------------------------------------------------------------
# User Response Model - Used to format the response data when fetching user details
# ----------------------------------------------------------------------------
class UserResponse(BaseModel):

    id: int  
    name: str  
    email: EmailStr  
    # password: str 
                   
    mob_number: str  
    role: str  
    created_at: datetime  
    updated_at: Optional[datetime]  

    class Config:
        """
        Configuration class to tell Pydantic to treat attributes as model fields.
        This is useful when data comes from a database and the attributes need to be mapped properly.
        """
        from_attributes = True

# ----------------------------------------------------------------------------
# User Update Model - Used to validate the data sent when updating user information
# ----------------------------------------------------------------------------
class UserUpdate(BaseModel):
  
    
    name: Optional[str] = None  # User's name (can be updated)
    email: Optional[EmailStr] = None  # User's email (can be updated)
    password: Optional[str] = None  # User's password (can be updated)
    mob_number: Optional[str] = None  # User's mobile number (can be updated)
    role: Optional[str] = None  # User's role (can be updated)

# ----------------------------------------------------------------------------
# User Login Model - Used to validate the data sent during user login
# ----------------------------------------------------------------------------
class UserLogin(BaseModel):
   
    email: str  # User's email (should match a registered email)
    password: str  # User's password (should match the stored password)

