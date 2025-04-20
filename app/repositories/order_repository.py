from sqlalchemy.orm import Session
from app.domain.models.orders import Order

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order_data: dict) -> Order:
        """Create a new order."""
        order = Order(**order_data)
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_order_by_id(self, order_id: int) -> Order:
        """Retrieve an order by its ID."""
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def get_all_orders(self) -> list:
        """Retrieve all orders."""
        return self.db.query(Order).all()

    def delete_order(self, order_id: int) -> None:
        """Delete an order by its ID."""
        order = self.get_order_by_id(order_id)
        if order:
            self.db.delete(order)
            self.db.commit()
