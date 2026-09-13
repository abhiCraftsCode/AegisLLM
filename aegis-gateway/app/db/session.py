from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine
from app.core.config import settings

# setup and intializing async engine #connect db
engine=create_async_engine(
  settings.DATABASE_URL,
  echo=False,
  future=True,
  pool_pre_ping=True,
  pool_size=10,
  max_overflow=20,
  pool_recycle=18000
)

LocalSession=async_sessionmaker(
  bind=engine,
  class_=AsyncSession,
  autocommit=False,
  autoflush=False,
  expire_on_commit=False,
)

#dependency helper function to connect to db
async def get_db()->AsyncGenerator[AsyncSession,None]:
  """dependency for db connection."""
  async with LocalSession() as session:
    try:
      yield session
    finally:
      await session.close()