from sqlalchemy.orm import Session
from app.domain.models.reservation import Reservation

class ReservationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_reservation(self, reservation_data: dict) -> Reservation:
        """Create a new reservation."""
        reservation = Reservation(**reservation_data)
        self.db.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation
    
    def get_reservation_by_id(self, reservation_id: int) -> Reservation:
        """Retrieve a reservation by its ID."""
        return self.db.query(Reservation).filter(Reservation.id == reservation_id).first()
    
    def get_all_reservations(self) -> list:
        """Retrieve all reservations."""
        return self.db.query(Reservation).all()

    def delete_reservation(self, reservation_id: int) -> None:
        """Delete a reservation by its ID."""
        reservation = self.get_reservation_by_id(reservation_id)
        if reservation:
            self.db.delete(reservation)
            self.db.commit()
