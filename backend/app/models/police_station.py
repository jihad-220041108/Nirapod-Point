
"""
Police Station Model
"""
from sqlalchemy import Column, String, Float, DateTime
import uuid
from datetime import datetime
from app.core.database import Base

class PoliceStation(Base):
    __tablename__ = "police_stations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    city = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)  # Ensure Float for coordinate math
    longitude = Column(Float, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
