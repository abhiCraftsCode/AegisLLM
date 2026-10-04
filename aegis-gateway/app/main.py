from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from app.core.config import settings
from app.core.engine import AegisEngine
from app.core.exceptions import AppException,exception_handler
from app.db import db_engine, Base
from app.api.router import api_router

# Lifespan context manager to auto-create DB tables on server startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[INFO] Aegis Gateway starting up...")
    app.state.engine=AegisEngine() # one engine for whole lifespan
    print("[DB] testing sql connections...")
    try:
      async with await asyncio.wait_for(
        db_engine.connect(),
        timeout=15
      ) as conn:
        print("[DB] db connection established.")
        #await conn.run_sync(Base.metadata.create_all)
        print("[DB] testing simple query...")
        await asyncio.wait_for(
            conn.exec_driver_sql("SELECT 1"),
            timeout=15
        )
        print("[DB] SELECT 1 successful.")
    except asyncio.TimeoutError:
        print("[DB] database operation timed out after 15 seconds.")
        raise
    except Exception as e:
        print("[DB] database connection/query failed:", repr(e))
        raise

    print("[DB] connection tested on db successfully.")
    yield
    print("[INFO] Aegis Gateway shutting down...")
    del app.state.engine
    await db_engine.dispose()

# main app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan
)

# centralised exception handling setup
@app.exception_handler(AppException)
async def app_exception_handler(request:Request,exc:AppException):
    return await exception_handler(request,exc)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Router ---
app.include_router(api_router)

@app.get("/")
def home():
    return {"If you are seeing this, it means server is running successfully."}