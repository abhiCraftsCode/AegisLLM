from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

from app.core.config import settings

print("[DB] DATABASE_URL type:", type(settings.DATABASE_URL))
print("[DB] DATABASE_URL present:", bool(settings.DATABASE_URL))
# setup and intializing async db engine #connect db
db_engine=create_async_engine(
  settings.DATABASE_URL,
  echo=False,
  future=True,
  pool_pre_ping=True,
  pool_size=2,#10
  max_overflow=3,#20
  pool_recycle=300
)

LocalSession=async_sessionmaker(
  bind=db_engine,
  class_=AsyncSession,
  autocommit=False,
  autoflush=False,
  expire_on_commit=False,
)


