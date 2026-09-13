from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db import engine, Base
from app.api.auth import auth_router

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

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Routers ---
app.include_router(auth_router)

@app.get("/")
def home():
    return {"if you are seeing this, it means server is running successfully."}