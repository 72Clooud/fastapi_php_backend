from database.database import db
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with db.get_session() as session:
        yield session 
