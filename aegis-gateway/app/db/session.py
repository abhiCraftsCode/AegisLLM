from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

from app.core.config import settings

from urllib.parse import urlparse

db_url = settings.DATABASE_URL
parsed = urlparse(db_url)

print("[DB] scheme:", parsed.scheme)
print("[DB] hostname present:", bool(parsed.hostname))
print("[DB] port:", parsed.port)
print("[DB] database present:", bool(parsed.path))
print("[DB] query params:", list(parsed.query.split("&")) if parsed.query else [])
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
  pool_recycle=300,
  connect_args={"timeout":10}
)

LocalSession=async_sessionmaker(
  bind=db_engine,
  class_=AsyncSession,
  autocommit=False,
  autoflush=False,
  expire_on_commit=False,
)


