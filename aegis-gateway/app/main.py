from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.exceptions import AppException,exception_handler
from app.db import engine, Base
from app.api.router import api_router

# Lifespan context manager to auto-create DB tables on server startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("[INFO] Aegis Gateway starting up...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    print("[INFO] Aegis Gateway shutting down...")
    await engine.dispose()

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