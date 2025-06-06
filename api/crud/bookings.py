from sqlalchemy.orm import Session

from api.database.models.bookings import Booking
from api.database.schemas.bookings import BookingCreate, BookingUpdate
from datetime import datetime



def create_booking(db: Session, booking: BookingCreate):
    new_booking = Booking(
        **booking.dict(),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

def get_bookings(db: Session):
    return db.query(Booking).all()

def get_booking(db: Session, booking_id: int):
    return db.query(Booking).filter(Booking.id == booking_id).first()
def update_booking(db: Session, booking_id: int, updated: BookingUpdate):
    db_booking = get_booking(db, booking_id)
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(db_booking, key, value)
    
    db_booking.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_booking)
    return db_booking

    
def delete_booking(db: Session, booking_id: int):
    db_booking = get_booking(db, booking_id)
    if db_booking:
        db.delete(db_booking)
        db.commit()
    return db_booking


def get_bookings_by_user(db: Session, user_id: int):
    return db.query(Booking).filter(Booking.user_id == user_id).all()
