"""
Tests for item service.
"""
from uuid import uuid4
from app.services.item_service import ItemService


def test_create_item():
    """Test creating an item in service."""
    service = ItemService()
    item = service.create("Test Item")
    assert item.name == "Test Item"
    assert item.id is not None
    assert item.created_at is not None


def test_get_item():
    """Test getting an item by ID."""
    service = ItemService()
    item = service.create("Test Item")
    retrieved = service.get_by_id(item.id)
    assert retrieved is not None
    assert retrieved.id == item.id
    assert retrieved.name == "Test Item"


def test_get_item_not_found():
    """Test getting non-existent item returns None."""
    service = ItemService()
    fake_id = uuid4()
    item = service.get_by_id(fake_id)
    assert item is None


def test_list_items():
    """Test listing all items."""
    service = ItemService()
    service.create("Item 1")
    service.create("Item 2")
    items = service.list_all()
    assert len(items) == 2


def test_delete_item():
    """Test deleting an item."""
    service = ItemService()
    item = service.create("Test Item")
    deleted = service.delete(item.id)
    assert deleted is True
    assert service.get_by_id(item.id) is None


def test_delete_item_not_found():
    """Test deleting non-existent item returns False."""
    service = ItemService()
    fake_id = uuid4()
    deleted = service.delete(fake_id)
    assert deleted is False

