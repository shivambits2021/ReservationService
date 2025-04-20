from fastapi import APIRouter
from app.api.v1.endpoints import reservation

api_router = APIRouter()

api_router.include_router(reservation.router, prefix="/reserve", tags=["reservations"])
