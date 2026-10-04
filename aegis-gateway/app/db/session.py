from sqlalchemy.ext.asyncio import async_sessionmaker,AsyncSession,create_async_engine

from app.core.config import settings

import asyncpg
import sqlalchemy

print("[DB] asyncpg version:", asyncpg.__version__)
print("[DB] SQLAlchemy version:", sqlalchemy.__version__)
import socket
db_host = settings.DATABASE_URL.split("@")[1].split("/")[0].split(":")[0]
try:
    sock = socket.create_connection((db_host, 5432), timeout=10)
    print("[DB] TCP connection to port 5432 successful.")
    sock.close()
except Exception as e:
    print("[DB] TCP connection failed:", repr(e))

print("[DB] testing hostname:", db_host)
from sqlalchemy.engine import make_url

parsed_db_url = make_url(settings.DATABASE_URL)

print("[DB] driver:", parsed_db_url.drivername)
print("[DB] host:", parsed_db_url.host)
print("[DB] port:", parsed_db_url.port)
print("[DB] database:", parsed_db_url.database)
print("[DB] username:", parsed_db_url.username)
print("[DB] password present:", bool(parsed_db_url.password))

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


