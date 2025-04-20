from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.order import OrderCreate, OrderResponse
from app.repositories.order_repository import OrderRepository
from app.db.session import get_db 
from app.repositories.product_repository import ProductRepository
from app.repositories.reservation_repository import ReservationRepository
from app.domain.services.reservation_service import ReservationService

router = APIRouter()

# Dependency to provide the repository
def get_order_repository(db: AsyncSession = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)

@router.post("/confirm-order", response_model=OrderResponse)
async def confirm_order(order_create: OrderCreate, order_repository: OrderRepository = Depends(get_order_repository)):
    # Use the repository method to create an order
    order_data = {"reservation_id": order_create.reservation_id}
    order = await order_repository.create_order(order_data)

    if not order:
        raise HTTPException(status_code=400, detail="Order creation failed")
    
    # Return the response model
    return OrderResponse.from_orm(order)


@router.post("/cancel-order/{reservation_id}")
async def cancel_order(
    reservation_id: int,
    db: AsyncSession = Depends(get_db)
):
    product_repo = ProductRepository(db)
    reservation_repo = ReservationRepository(db)
    reservation_service = ReservationService(db, product_repo, reservation_repo)

    return await reservation_service.cancel_reservation(reservation_id)

