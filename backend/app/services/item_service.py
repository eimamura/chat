"""
Item service for business logic.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.item import Item
from app.models.db_item import DBItem


class ItemService:
    """Service for managing items with database persistence."""
    
    def __init__(self, db: Session):
        """Initialize with database session."""
        self.db = db
    
    def list_all(self) -> List[Item]:
        """List all items."""
        db_items = self.db.query(DBItem).order_by(DBItem.created_at.desc()).all()
        return [
            Item(
                name=db_item.name,
                item_id=db_item.id,
                created_at=db_item.created_at
            )
            for db_item in db_items
        ]
    
    def get_by_id(self, item_id: UUID) -> Optional[Item]:
        """Get an item by ID."""
        db_item = self.db.query(DBItem).filter(DBItem.id == item_id).first()
        if not db_item:
            return None
        return Item(
            name=db_item.name,
            item_id=db_item.id,
            created_at=db_item.created_at
        )
    
    def create(self, name: str) -> Item:
        """Create a new item."""
        db_item = DBItem(name=name)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return Item(
            name=db_item.name,
            item_id=db_item.id,
            created_at=db_item.created_at
        )
    
    def delete(self, item_id: UUID) -> bool:
        """Delete an item by ID. Returns True if deleted, False if not found."""
        db_item = self.db.query(DBItem).filter(DBItem.id == item_id).first()
        if not db_item:
            return False
        self.db.delete(db_item)
        self.db.commit()
        return True

