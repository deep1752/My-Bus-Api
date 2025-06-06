from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from api.database.connection import Base

class Travel(Base):
    __tablename__ = "travels"

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String(255),nullable=False)
    from_location = Column(String(255),nullable=False)
    to_location = Column(String(255),nullable=False)
    time = Column(String(255),nullable=False)
    seats = Column(Integer,nullable=False)
    price = Column(Float,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

