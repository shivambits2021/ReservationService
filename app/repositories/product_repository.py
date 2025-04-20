from sqlalchemy.ext.asyncio import AsyncSession
from app.domain.models.product import Product
from sqlalchemy.future import select

class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_product_by_id(self, product_id: int) -> Product:
        """Fetch a product by ID."""
        stmt = select(Product).filter(Product.id == product_id)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update_product_stock(self, product_id: int, quantity: int) -> None:
        """Reduce the stock of a product."""
        product = await self.get_product_by_id(product_id)  # Awaiting the async function
        if product:
            product.stock -= quantity
            await self.db.commit()  # Ensure commit is awaited in async session
            await self.db.refresh(product)  # Refresh after commit to reflect changes

    async def create_product(self, product_data: dict) -> Product:
        """Create a new product."""
        product = Product(**product_data)
        self.db.add(product)
        await self.db.commit()  # Commit asynchronously
        await self.db.refresh(product)  # Refresh asynchronously to load the latest state
        return product
