"""
Item model and schemas.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    """Base item schema."""
    name: str = Field(..., min_length=1, max_length=200, description="Item name")


class ItemCreate(ItemBase):
    """Schema for creating an item."""
    pass


class ItemResponse(ItemBase):
    """Schema for item response."""
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class Item:
    """In-memory item model."""
    def __init__(self, name: str, item_id: Optional[UUID] = None, created_at: Optional[datetime] = None):
        self.id = item_id or uuid4()
        self.name = name
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> dict:
        """Convert item to dictionary."""
        return {
            "id": str(self.id),
            "name": self.name,
            "created_at": self.created_at.isoformat()
        }

