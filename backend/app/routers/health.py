"""
Health check endpoint.
"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"


@router.get("/healthz", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.
    Returns 200 if the API is up and running.
    """
    return HealthResponse(status="ok")

