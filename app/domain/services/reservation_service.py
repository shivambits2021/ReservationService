from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
import pytz
from app.repositories.product_repository import ProductRepository
from app.repositories.reservation_repository import ReservationRepository
from app.schemas.reservation import ReservationCreate, ReservationResponse,ReservationStatus
from app.domain.models.reservation import Reservation
from app.domain.models.product import Product
from sqlalchemy import select
from fastapi import HTTPException

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
        
        """Reserve a product for a customer."""
        product = await self.product_repo.get_product_by_id(data.product_id)
        if not product:
            raise ValueError("Product not found")

        if product.stock < data.quantity:
            raise ValueError("Insufficient stock")

        # Reduce stock and commit asynchronously
        product.stock -= data.quantity
        await self.db.commit()
        await self.db.refresh(product)

        # Set expiration time for the reservation (make sure it’s timezone-aware)
        expires_at = datetime.now(pytz.utc) + timedelta(seconds=20)
        
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

    async def release_expired_reservations(self) -> None:
        """Release expired reservations that are older than the allowed time."""
        try:
            stmt = select(Reservation).filter(Reservation.status == 'pending')
            result = await self.db.execute(stmt)
            reservations = result.scalars().all()

            utc_now = datetime.now(pytz.utc)  # Make sure this is timezone-aware

            for reservation in reservations:
                # Ensure reservation.expires_at is timezone-aware
                expires_at_utc = reservation.expires_at.astimezone(pytz.utc) if reservation.expires_at.tzinfo is None else reservation.expires_at

                # Check if the reservation has expired
                if expires_at_utc < utc_now:
                    # Update the reservation status to 'cancelled_by_timeout'
                    reservation.status = 'cancelled_by_timeout'
                    await self.db.commit()

                    # Release the product back to inventory
                    await self._release_product(reservation.product_id, reservation.quantity)

        except Exception as e:
            await self.db.rollback()
            raise e

    async def _release_product(self, product_id: int, quantity: int) -> None:
        """Helper method to release the product back into inventory after timeout."""
        try:
            stmt = select(Product).filter(Product.id == product_id)
            result = await self.db.execute(stmt)
            product = result.scalars().first()

            if product:
                # Increase the stock of the product
                product.stock += quantity
                await self.db.commit()
        except Exception as e:
            await self.db.rollback()
            raise e
        
        
    async def cancel_reservation(self, reservation_id: int):
        reservation = await self.reservation_repo.get_reservation_by_id(reservation_id)
        if not reservation:
            raise HTTPException(status_code=404, detail="Reservation not found")

        if reservation.status != ReservationStatus.PENDING:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot cancel reservation with status '{reservation.status}'"
            )

        await self.product_repo.update_product_stock(reservation.product_id, reservation.quantity)
        await self.reservation_repo.cancel_reservation(reservation)
        return reservation
