from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.order import OrderCreate, OrderResponse
from app.repositories.order_repository import OrderRepository
from app.db.session import get_db 

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
