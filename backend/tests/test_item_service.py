"""
Tests for item service.
"""
from uuid import uuid4
from sqlalchemy.orm import Session
from app.services.item_service import ItemService
from app.database import engine, Base
from app.models.db_item import DBItem

# Create test database
Base.metadata.create_all(bind=engine)


def get_test_db():
    """Get test database session."""
    return Session(bind=engine)


def test_create_item():
    """Test creating an item in service."""
    db = get_test_db()
    try:
        service = ItemService(db)
        item = service.create("Test Item")
        assert item.name == "Test Item"
        assert item.id is not None
        assert item.created_at is not None
    finally:
        db.close()


def test_get_item():
    """Test getting an item by ID."""
    db = get_test_db()
    try:
        service = ItemService(db)
        item = service.create("Test Item")
        retrieved = service.get_by_id(item.id)
        assert retrieved is not None
        assert retrieved.id == item.id
        assert retrieved.name == "Test Item"
    finally:
        db.close()


def test_get_item_not_found():
    """Test getting non-existent item returns None."""
    db = get_test_db()
    try:
        service = ItemService(db)
        fake_id = uuid4()
        item = service.get_by_id(fake_id)
        assert item is None
    finally:
        db.close()


def test_list_items():
    """Test listing all items."""
    db = get_test_db()
    try:
        service = ItemService(db)
        service.create("Item 1")
        service.create("Item 2")
        items = service.list_all()
        assert len(items) >= 2
    finally:
        db.close()


def test_delete_item():
    """Test deleting an item."""
    db = get_test_db()
    try:
        service = ItemService(db)
        item = service.create("Test Item")
        deleted = service.delete(item.id)
        assert deleted is True
        assert service.get_by_id(item.id) is None
    finally:
        db.close()


def test_delete_item_not_found():
    """Test deleting non-existent item returns False."""
    db = get_test_db()
    try:
        service = ItemService(db)
        fake_id = uuid4()
        deleted = service.delete(fake_id)
        assert deleted is False
    finally:
        db.close()

