from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ----- Travel -----
class TravelBase(BaseModel):
    image: str
    from_location: str
    to_location: str
    time: str
    seats: int
    price: float
    created_at: datetime
    updated_at : datetime




class TravelCreate(TravelBase):
    pass

class TravelUpdate(BaseModel):  # <- Inherit from BaseModel directly
   
    image: Optional[str] = None
    from_location: Optional[str] = None
    to_location: Optional[str] = None
    time: Optional[str] = None
    seats: Optional[int] = None  # <- Make it optional
    price: Optional[float] = None
class TravelOut(TravelBase):
    id: int

    class Config:
        from_attributes = True
