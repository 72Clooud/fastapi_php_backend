from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession 
from core.config import settings
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AsyncDatabaseSession:
    def __init__(self):
        self._engine = create_async_engine(
            f"postgresql+asyncpg://{settings.db_user}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}",
            echo=True
        )

        self._SessionLocal = async_sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
       
    async def init(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    def get_session(self) -> AsyncSession:
        return self._SessionLocal()
        
db = AsyncDatabaseSession()