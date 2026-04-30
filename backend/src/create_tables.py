import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

from .database import Base
from .config import settings

async def create_tables():
    engine = create_async_engine(settings.database_url, echo=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await engine.dispose()
    print("Tables created successfully")

if __name__ == "__main__":
    asyncio.run(create_tables())
