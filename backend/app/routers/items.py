"""
Item CRUD endpoints.
"""
from typing import List
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
import logging

from app.models.item import ItemCreate, ItemResponse
from app.services.item_service import ItemService
from app.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/items", response_model=List[ItemResponse])
async def list_items(db: Session = Depends(get_db)):
    """
    List all items.
    """
    try:
        service = ItemService(db)
        items = service.list_all()
        return [ItemResponse(id=item.id, name=item.name, created_at=item.created_at) for item in items]
    except Exception as e:
        logger.error(f"Error listing items: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list items"
        )


@router.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item.
    """
    try:
        service = ItemService(db)
        new_item = service.create(item.name)
        logger.info(f"Created item: {new_item.id}")
        return ItemResponse(id=new_item.id, name=new_item.name, created_at=new_item.created_at)
    except Exception as e:
        logger.error(f"Error creating item: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create item"
        )


@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: UUID, db: Session = Depends(get_db)):
    """
    Get a specific item by ID.
    """
    try:
        service = ItemService(db)
        item = service.get_by_id(item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found"
            )
        return ItemResponse(id=item.id, name=item.name, created_at=item.created_at)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting item: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get item"
        )


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: UUID, db: Session = Depends(get_db)):
    """
    Delete an item by ID.
    """
    try:
        service = ItemService(db)
        deleted = service.delete(item_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with id {item_id} not found"
            )
        logger.info(f"Deleted item: {item_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting item: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete item"
        )

