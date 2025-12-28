"""
Message model and schemas for chat.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    """Base message schema."""
    username: str = Field(..., min_length=1, max_length=50, description="Username")
    content: str = Field(..., min_length=1, max_length=1000, description="Message content")


class MessageCreate(MessageBase):
    """Schema for creating a message."""
    pass


class MessageResponse(MessageBase):
    """Schema for message response."""
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


class Message:
    """Message model."""
    def __init__(
        self,
        username: str,
        content: str,
        message_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None
    ):
        self.id = message_id or uuid4()
        self.username = username
        self.content = content
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self) -> dict:
        """Convert message to dictionary."""
        return {
            "id": str(self.id),
            "username": self.username,
            "content": self.content,
            "created_at": self.created_at.isoformat()
        }

