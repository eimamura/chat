"""
Tests for item endpoints.
"""
from uuid import uuid4
from fastapi.testclient import TestClient
from main import app
from app.services.item_service import ItemService

client = TestClient(app)


def test_create_item():
    """Test creating an item."""
    response = client.post("/api/items", json={"name": "Test Item"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data
    assert "created_at" in data


def test_list_items():
    """Test listing items."""
    # Create an item first
    create_response = client.post("/api/items", json={"name": "List Test Item"})
    assert create_response.status_code == 201
    
    # List items
    response = client.get("/api/items")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    assert len(items) > 0


def test_get_item():
    """Test getting a specific item."""
    # Create an item
    create_response = client.post("/api/items", json={"name": "Get Test Item"})
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # Get the item
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Get Test Item"


def test_get_item_not_found():
    """Test getting a non-existent item returns 404."""
    fake_id = str(uuid4())
    response = client.get(f"/api/items/{fake_id}")
    assert response.status_code == 404


def test_delete_item():
    """Test deleting an item."""
    # Create an item
    create_response = client.post("/api/items", json={"name": "Delete Test Item"})
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # Delete the item
    response = client.delete(f"/api/items/{item_id}")
    assert response.status_code == 204
    
    # Verify it's deleted
    get_response = client.get(f"/api/items/{item_id}")
    assert get_response.status_code == 404


def test_delete_item_not_found():
    """Test deleting a non-existent item returns 404."""
    fake_id = str(uuid4())
    response = client.delete(f"/api/items/{fake_id}")
    assert response.status_code == 404


def test_create_item_validation():
    """Test item creation validation."""
    # Empty name should fail
    response = client.post("/api/items", json={"name": ""})
    assert response.status_code == 422
    
    # Missing name should fail
    response = client.post("/api/items", json={})
    assert response.status_code == 422

