from pydantic import BaseModel
from datetime import datetime

class OrderCreate(BaseModel):
    reservation_id: int

class OrderResponse(BaseModel):
    id: int
    reservation_id: int
    created_at: datetime

class CancelOrderRequest(BaseModel):
    reservation_id: int


    class Config:
        from_attributes = True
