from pydantic import BaseModel
from datetime import datetime
from typing import Optional



# ----- Booking -----
class BookingBase(BaseModel):
    user_id: int
    from_location: str
    to_location: str
    seats: int
    price_per_seat: float
    total_price: float
 


class BookingCreate(BookingBase):
    pass


class BookingUpdate(BaseModel):
    user_id: int
    from_location: str
    to_location: str
    seats: int
    price_per_seat: float
    total_price: float
    updated_at: datetime



class BookingOut(BookingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
