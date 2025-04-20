from fastapi import APIRouter
from app.api.v1.endpoints import reservation,order

api_router = APIRouter()

api_router.include_router(reservation.router, prefix="/reserve", tags=["reservations"])
api_router.include_router(order.router, prefix="/order", tags=["orders"])