from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.models.orders import Order
from app.domain.models.reservation import Reservation  # Assuming Reservation model exists
from fastapi import HTTPException, status

class OrderRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_order(self, order_data: dict) -> Order:
        """Create a new order only if the reservation exists and has a 'pending' status."""
        try:
            # Check if reservation_id exists in the order_data
            if 'reservation_id' not in order_data:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="reservation_id must be provided")
            
            # Fetch the reservation and check its current status
            stmt = select(Reservation).filter(Reservation.id == order_data['reservation_id'])
            result = await self.db.execute(stmt)
            reservation = result.scalars().first()

            if reservation:
                # Ensure that the reservation is 'pending' before creating the order
                if reservation.status != 'pending':
                    # Raise HTTP exception for invalid reservation status
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Cannot create order. Reservation status is not 'pending', it is '{reservation.status}'."
                    )

                # Proceed to create the order if the reservation is 'pending'
                order_data.setdefault('status', 'confirmed')  # Set order status to 'confirmed'
                order_data.setdefault('customer_email', 'default@gmail.com')  # Default email if not provided
                
                order = Order(**order_data)

                # Update the reservation status to 'confirmed' after order creation
                reservation.status = 'confirmed'
                await self.db.commit()  # Commit the status change for the reservation

                # Add the order to the session and commit
                self.db.add(order)
                await self.db.commit()
                await self.db.refresh(order)
                return order
            else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found for the provided reservation_id.")

        except HTTPException as e:
            # Handle HTTPException raised above
            raise e
        except Exception as e:
            await self.db.rollback()  # Rollback in case of error
            # Log the error (if needed) or re-raise the exception
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def get_order_by_id(self, order_id: int) -> Order:
        """Retrieve an order by its ID."""
        try:
            stmt = select(Order).filter(Order.id == order_id)
            result = await self.db.execute(stmt)
            return result.scalars().first()  # Get the first result
        except Exception as e:
            raise e

    async def get_all_orders(self) -> list:
        """Retrieve all orders."""
        try:
            stmt = select(Order)
            result = await self.db.execute(stmt)
            return result.scalars().all()  # Get all results
        except Exception as e:
            raise e

    async def delete_order(self, order_id: int) -> None:
        """Delete an order by its ID."""
        try:
            order = await self.get_order_by_id(order_id)
            if order:
                await self.db.delete(order)
                await self.db.commit()  # Ensure async commit
        except Exception as e:
            await self.db.rollback()  # Rollback in case of error
            raise e
