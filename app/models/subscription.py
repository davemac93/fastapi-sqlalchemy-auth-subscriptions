import uuid
import enum

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, Text, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.core.database import Base

class PlansOptions(str, enum.Enum):
    BASIC = "basic"
    GOLD = "gold"
    PLATINIUM = "platinium"

class PlansPrices(float, enum.Enum):
    BASIC = 0.00
    GOLD = 5.99
    PLATINIUM = 12.99

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    price = Column(Float, nullable=False, default=PlansPrices.BASIC)
    option = Column(Enum(PlansOptions), nullable=False, default=PlansOptions.BASIC)
    created_at = Column(String, nullable=False, default=datetime.now())
    modified_at = Column(String, nullable=False, default=datetime.now())

    user_id = Column(String, ForeignKey("users.id"))

    owner = relationship("User", back_populates="subscriptions")
