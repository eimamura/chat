"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import os

from app.routers import health, items
from app.database import engine, Base

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="MVP API",
    description="Minimal MVP API for Item CRUD operations",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(items.router, prefix="/api", tags=["items"])


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Starting MVP API...")
    # Run migrations
    try:
        from alembic.config import Config
        from alembic import command
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed.")
        
        # Run seed script if in development
        if os.getenv("RUN_SEED", "false").lower() == "true":
            from scripts.seed import seed_database
            seed_database()
            logger.info("Database seeded with demo data.")
    except Exception as e:
        logger.warning(f"Migration/seed error (may be expected): {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Shutting down MVP API...")

