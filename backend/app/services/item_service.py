"""
Item service for business logic.
"""
from typing import List, Optional
from uuid import UUID
from app.models.item import Item


class ItemService:
    """Service for managing items (in-memory for now)."""
    
    def __init__(self):
        """Initialize with empty storage."""
        self._items: dict[UUID, Item] = {}
    
    def list_all(self) -> List[Item]:
        """List all items."""
        return list(self._items.values())
    
    def get_by_id(self, item_id: UUID) -> Optional[Item]:
        """Get an item by ID."""
        return self._items.get(item_id)
    
    def create(self, name: str) -> Item:
        """Create a new item."""
        item = Item(name=name)
        self._items[item.id] = item
        return item
    
    def delete(self, item_id: UUID) -> bool:
        """Delete an item by ID. Returns True if deleted, False if not found."""
        if item_id in self._items:
            del self._items[item_id]
            return True
        return False

