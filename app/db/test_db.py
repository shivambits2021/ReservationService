import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import get_db

async def test_db_connection():
    # Using the async generator to get a database session
    async for db in get_db():
        print("Connection successful!")
        # Example: Execute a simple query using text()
        result = await db.execute(text('SELECT 1'))
        print("Query result:", result.fetchall())  # This should return [(1,)]
        break

# Run the test function asynchronously
if __name__ == "__main__":
    asyncio.run(test_db_connection())
