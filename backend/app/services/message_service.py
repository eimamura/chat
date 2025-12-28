"""
Message service for business logic.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.message import Message
from app.models.db_message import DBMessage


class MessageService:
    """Service for managing messages with database persistence."""
    
    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
    
    def list_all(self, limit: Optional[int] = None) -> List[Message]:
        """List all messages, ordered by creation time (newest first)."""
        query = self.db.query(DBMessage).order_by(DBMessage.created_at.desc())
        if limit:
            query = query.limit(limit)
        db_messages = query.all()
        # Reverse to show oldest first (chronological order)
        db_messages.reverse()
        return [
            Message(
                username=db_msg.username,
                content=db_msg.content,
                message_id=db_msg.id,
                created_at=db_msg.created_at
            )
            for db_msg in db_messages
        ]
    
    def get_by_id(self, message_id: UUID) -> Optional[Message]:
        """Get a message by ID."""
        db_message = self.db.query(DBMessage).filter(DBMessage.id == message_id).first()
        if not db_message:
            return None
        return Message(
            username=db_message.username,
            content=db_message.content,
            message_id=db_message.id,
            created_at=db_message.created_at
        )
    
    def create(self, username: str, content: str) -> Message:
        """Create a new message."""
        db_message = DBMessage(username=username, content=content)
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return Message(
            username=db_message.username,
            content=db_message.content,
            message_id=db_message.id,
            created_at=db_message.created_at
        )
    
    def delete(self, message_id: UUID) -> bool:
        """Delete a message by ID. Returns True if deleted, False if not found."""
        db_message = self.db.query(DBMessage).filter(DBMessage.id == message_id).first()
        if not db_message:
            return False
        self.db.delete(db_message)
        self.db.commit()
        return True
    
    def delete_all(self) -> int:
        """Delete all messages. Returns the number of deleted messages."""
        count = self.db.query(DBMessage).count()
        self.db.query(DBMessage).delete()
        self.db.commit()
        return count
