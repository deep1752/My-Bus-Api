from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.database.schemas.contact import ContactCreate, ContactResponse
from api.crud.contact import create_contact
from api.database.connection import get_db


router = APIRouter()

@router.post("/", response_model=ContactResponse)
def submit_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db, contact)
