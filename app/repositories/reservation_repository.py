from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.models.reservation import Reservation
from sqlalchemy.orm import selectinload

class ReservationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_reservation(self, reservation_data: dict) -> Reservation:
        """Create a new reservation."""
        reservation = Reservation(**reservation_data)
        self.db.add(reservation)
        await self.db.commit()  # Commit asynchronously
        await self.db.refresh(reservation)  # Refresh asynchronously
        return reservation
    
    async def get_reservation_by_id(self, reservation_id: int) -> Reservation:
        """Retrieve a reservation by its ID."""
        result = await self.db.execute(
            select(Reservation).filter(Reservation.id == reservation_id)
        )
        return result.scalars().first()  # Using scalars to get the first result

    async def get_all_reservations(self) -> list:
        """Retrieve all reservations."""
        result = await self.db.execute(select(Reservation))
        return result.scalars().all()  # Using scalars to fetch all results

    async def delete_reservation(self, reservation_id: int) -> None:
        """Delete a reservation by its ID."""
        reservation = await self.get_reservation_by_id(reservation_id)
        if reservation:
            await self.db.delete(reservation)  # Delete asynchronously
            await self.db.commit()  # Commit asynchronously
