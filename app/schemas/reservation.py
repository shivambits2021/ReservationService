from pydantic import BaseModel
from datetime import datetime

class ReservationCreate(BaseModel):
    product_id: int
    quantity: int


class ReservationResponse(BaseModel):
    reservation_id: int
    product_id: int
    quantity: int
    status: str
    expires_at: datetime

    class Config:
        orm_mode = True  # Enables SQLAlchemy model conversion
