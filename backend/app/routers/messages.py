"""
Message CRUD endpoints for chat.
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.orm import Session
import logging

from app.models.message import MessageCreate, MessageResponse
from app.services.message_service import MessageService
from app.database import get_db

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/messages", response_model=List[MessageResponse])
async def list_messages(
    limit: Optional[int] = Query(None, ge=1, le=100, description="Limit number of messages"),
    db: Session = Depends(get_db)
):
    """
    List all messages, ordered chronologically (oldest first).
    """
    try:
        logger.info(f"Listing messages (limit={limit})")
        service = MessageService(db)
        messages = service.list_all(limit=limit)
        logger.info(f"Found {len(messages)} messages")
        return [
            MessageResponse(
                id=msg.id,
                username=msg.username,
                content=msg.content,
                created_at=msg.created_at
            )
            for msg in messages
        ]
    except Exception as e:
        logger.error(f"Error listing messages: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to list messages"
        )


@router.post("/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    """
    Create a new message.
    """
    try:
        logger.info(f"Creating message from user: {message.username}")
        service = MessageService(db)
        new_message = service.create(message.username, message.content)
        logger.info(f"Created message: id={new_message.id}, username={new_message.username}")
        return MessageResponse(
            id=new_message.id,
            username=new_message.username,
            content=new_message.content,
            created_at=new_message.created_at
        )
    except Exception as e:
        logger.error(f"Error creating message: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create message"
        )


@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: UUID, db: Session = Depends(get_db)):
    """
    Get a specific message by ID.
    """
    try:
        logger.info(f"Getting message: {message_id}")
        service = MessageService(db)
        message = service.get_by_id(message_id)
        if not message:
            logger.warning(f"Message not found: {message_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Message with id {message_id} not found"
            )
        logger.info(f"Found message: id={message.id}, username={message.username}")
        return MessageResponse(
            id=message.id,
            username=message.username,
            content=message.content,
            created_at=message.created_at
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting message: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get message"
        )


@router.delete("/messages/{message_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(message_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a message by ID.
    """
    try:
        logger.info(f"Deleting message: {message_id}")
        service = MessageService(db)
        deleted = service.delete(message_id)
        if not deleted:
            logger.warning(f"Message not found for deletion: {message_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Message with id {message_id} not found"
            )
        logger.info(f"Deleted message: {message_id}")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting message: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete message"
        )

