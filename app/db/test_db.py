import asyncpg
import asyncio

async def test_connection():
    try:
        # Attempt to connect to the PostgreSQL database using asyncpg
        conn = await asyncpg.connect('postgresql://postgres:Bits2019%40%21@localhost:5432/reservation')
        print("Connection successful!")
        await conn.close()
    except Exception as e:
        print(f"Failed to connect: {e}")

# Run the test function
loop = asyncio.get_event_loop()
loop.run_until_complete(test_connection())
