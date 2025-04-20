from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.order_repository import OrderRepository
from app.schemas.order import OrderCreate, OrderResponse
from app.domain.models.orders import Order

class OrderService:
    def __init__(self, db: AsyncSession, order_repo: OrderRepository):
        self.db = db
        self.order_repo = order_repo

    async def create_order(self, data: OrderCreate) -> OrderResponse:
        # Create the order in the database
        order_data = {"reservation_id": data.reservation_id}
        order = await self.order_repo.create_order(order_data)

        # Convert SQLAlchemy model to Pydantic model before returning
        return OrderResponse.model_validate(order)  # Use model_validate to serialize the SQLAlchemy object

