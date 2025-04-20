from sqlalchemy.orm import Session
from app.domain.models.product import Product

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_product_by_id(self, product_id: int) -> Product:
        """Retrieve a product by its ID."""
        return self.db.query(Product).filter(Product.id == product_id).first()

    def update_product_stock(self, product_id: int, quantity: int) -> None:
        """Reduce the stock of a product."""
        product = self.get_product_by_id(product_id)
        if product:
            product.stock -= quantity
            self.db.commit()
            self.db.refresh(product)
    
    def create_product(self, product_data: dict) -> Product:
        """Create a new product."""
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
