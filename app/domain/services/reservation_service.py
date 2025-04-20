from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.repositories.product_repository import ProductRepository
from app.repositories.reservation_repository import ReservationRepository
from app.schemas.reservation import ReservationCreate, ReservationResponse

class ReservationService:
    def __init__(
        self,
        db: AsyncSession,
        product_repo: ProductRepository,
        reservation_repo: ReservationRepository,
    ):
        self.db = db
        self.product_repo = product_repo
        self.reservation_repo = reservation_repo

    async def reserve_product(self, data: ReservationCreate) -> ReservationResponse:
        product = await self.product_repo.get_product_by_id(data.product_id)
        if not product:
            raise ValueError("Product not found")

        if product.stock < data.quantity:
            raise ValueError("Insufficient stock")

        # Reduce stock and commit asynchronously
        product.stock -= data.quantity
        await self.db.commit()
        await self.db.refresh(product)

        # Set expiration time for the reservation
        expires_at = datetime.utcnow() + timedelta(minutes=15)
        
        # Create reservation asynchronously
        reservation = await self.reservation_repo.create_reservation({
            "product_id": data.product_id,
            "quantity": data.quantity,
            "expires_at": expires_at,
        })

        # Return ReservationResponse
        return ReservationResponse(
            reservation_id=reservation.id,
            product_id=reservation.product_id,
            quantity=reservation.quantity,
            status=reservation.status,
            expires_at=reservation.expires_at
        )
