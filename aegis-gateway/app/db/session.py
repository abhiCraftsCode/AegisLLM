from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine
from app.core.config import settings

# setup and intializing async engine #connect db
engine=create_async_engine(
  settings.DATABASE_URL,
  echo=False,
  future=True,
)

LocalSession=async_sessionmaker(
  bind=engine,
  class_=AsyncSession,
  expire_on_commit=False
)

#dependency helper function to connect to db
async def get_db()->AsyncGenerator[AsyncSession,None]:
  """dependency for db connection."""
  async with LocalSession() as session:
    try:
      yield session
      await session.commit()
    except Exception:
      await session.rollback()
      raise
    finally:
      await session.close()