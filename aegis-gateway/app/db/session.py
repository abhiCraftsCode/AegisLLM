from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

from app.core.config import settings

import socket

db_host = settings.DATABASE_URL.split("@")[1].split("/")[0].split(":")[0]

print("[DB] testing hostname:", db_host)

try:
    result = socket.getaddrinfo(db_host, 5432)
    print("[DB] DNS resolution successful:", result[0][4])
except Exception as e:
    print("[DB] DNS resolution failed:", repr(e))
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


