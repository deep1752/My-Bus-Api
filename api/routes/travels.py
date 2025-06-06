from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.schemas.travels import TravelCreate, TravelOut, TravelUpdate
from api.crud import travels
from api.database.connection import get_db

router = APIRouter()

@router.post("/post", response_model=TravelOut)
def create(travel: TravelCreate, db: Session = Depends(get_db)):
    return travels.create_travel(db, travel)

@router.get("/get", response_model=list[TravelOut])
def get_all(db: Session = Depends(get_db)):
    return travels.get_travels(db)

@router.get("/get_by_id/{travel_id}", response_model=TravelOut)
def get(travel_id: int, db: Session = Depends(get_db)):
    travel = travels.get_travel(db, travel_id)
    if not travel:
        raise HTTPException(status_code=404, detail="Travel not found")
    return travel

    
@router.put("/update/{travel_id}", response_model=TravelOut)
def update_seats(travel_id: int, updated: TravelUpdate, db: Session = Depends(get_db)):
    return travels.update_travel(db, travel_id, updated)


@router.delete("/delete/{travel_id}")
def delete(travel_id: int, db: Session = Depends(get_db)):
    travels.delete_travel(db, travel_id)
    return {"message": "Travel deleted"}

