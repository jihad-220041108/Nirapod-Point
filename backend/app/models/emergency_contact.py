"""
Emergency contact model
"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship as sa_relationship
import uuid
from app.core.database import Base


from sqlalchemy.dialects.postgresql import UUID

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    
    id = Column(UUID(as_uuid=False), primary_key=True, default=lambda: str(uuid.uuid4()))
    # user_id is UUID in this table, but users.id is String. 
    # We keep this as UUID so queries against this table cast correcty.
    user_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    relationship = Column(String)
    
    # Relationships
    user = sa_relationship("User", back_populates="emergency_contacts")
