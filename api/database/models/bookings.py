from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from api.database.connection import Base

class Booking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    from_location = Column(String(255),nullable=False)
    to_location = Column(String(255),nullable=False)
    seats = Column(Integer,nullable=False)
    price_per_seat = Column(Float,nullable=False)
    total_price = Column(Float,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

