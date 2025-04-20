from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class ReservationCreate(BaseModel):
    product_id: int
    quantity: int


class ReservationResponse(BaseModel):
    reservation_id: int
    product_id: int
    quantity: int
    status: str
    expires_at: datetime
    
class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


    class Config:
        orm_mode = True  # Enables SQLAlchemy model conversion
