from sqlalchemy.orm import Session
from api.database.models.travels import Travel
from api.database.schemas.travels import TravelCreate, TravelUpdate


def create_travel(db: Session, travel: TravelCreate):
    new_travel = Travel(**travel.dict())
    db.add(new_travel)
    db.commit()
    db.refresh(new_travel)
    return new_travel

def get_travels(db: Session):
    return db.query(Travel).all()

def get_travel(db: Session, travel_id: int):
    return db.query(Travel).filter(Travel.id == travel_id).first()

    
def update_travel(db: Session, travel_id: int, updated: TravelUpdate):
    db_travel = get_travel(db, travel_id)
    if db_travel:
        update_data = updated.dict(exclude_unset=True)  # only include provided fields
        for key, value in update_data.items():
            setattr(db_travel, key, value)
        db.commit()
        db.refresh(db_travel)
    return db_travel


def delete_travel(db: Session, travel_id: int):
    db_travel = get_travel(db, travel_id)
    if db_travel:
        db.delete(db_travel)
        db.commit()
    return db_travel
