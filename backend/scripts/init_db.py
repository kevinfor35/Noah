import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.database import Base, async_session_maker
from src.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import select
from src.security import get_password_hash
from src.models import User

async def create_admin_user():
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.email == 'admin@example.com')
        )
        existing_admin = result.scalar_one_or_none()
        
        if existing_admin:
            print("Admin user already exists")
            return
        
        hashed_password = get_password_hash('admin123')
        admin_user = User(
            email='admin@example.com',
            username='admin',
            hashed_password=hashed_password,
            is_admin=True
        )
        session.add(admin_user)
        await session.commit()
        print("Admin user created: admin@example.com / admin123")

async def main():
    print("Creating database tables...")
    
    engine = create_async_engine(settings.database_url, echo=True)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    await engine.dispose()
    
    print("Tables created successfully")
    
    await create_admin_user()

if __name__ == "__main__":
    asyncio.run(main())
