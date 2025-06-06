from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.schemas.bookings import BookingCreate, BookingOut, BookingUpdate
from api.crud import bookings
from api.database.connection import get_db


router = APIRouter()

@router.post("/post", response_model=BookingOut)
def create(booking: BookingCreate, db: Session = Depends(get_db)):
    return bookings.create_booking(db, booking)

@router.get("/get", response_model=list[BookingOut])
def get_all(db: Session = Depends(get_db)):
    return bookings.get_bookings(db)

@router.get("/get_by_id/{booking_id}", response_model=BookingOut)
def get(booking_id: int, db: Session = Depends(get_db)):
    booking = bookings.get_booking(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking

@router.put("/update/{booking_id}", response_model=BookingOut)
def update(booking_id: int, updated: BookingUpdate, db: Session = Depends(get_db)):
    return bookings.update_booking(db, booking_id, updated)

@router.delete("/delete/{booking_id}")
def delete(booking_id: int, db: Session = Depends(get_db)):
    bookings.delete_booking(db, booking_id)
    return {"message": "Booking deleted"}





@router.get("/user/{user_id}", response_model=list[BookingOut])
def get_bookings_by_user(user_id: int, db: Session = Depends(get_db)):
    return bookings.get_bookings_by_user(db, user_id)
