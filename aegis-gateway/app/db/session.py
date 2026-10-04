from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

from app.core.config import settings

# setup and intializing async db engine #connect db
db_engine=create_async_engine(
  settings.DATABASE_URL,
  echo=False,
  future=True,
  pool_pre_ping=True,
  pool_size=2,#10
  max_overflow=3,#20
  pool_recycle=300,
  connect_args={"timeout":10,"ssl":"require"}
)

LocalSession=async_sessionmaker(
  bind=db_engine,
  class_=AsyncSession,
  autocommit=False,
  autoflush=False,
  expire_on_commit=False,
)


