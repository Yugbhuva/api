from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import logging

from app.schemas.item import ItemResponse, ItemCreate, ItemUpdate
from app.services.item_service import ItemService
from app.core.config import get_settings

logger = logging.getLogger("fastapi_app")
router = APIRouter(prefix="/items", tags=["items"])

# Database dependency
async def get_database():
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
    from sqlalchemy.orm import sessionmaker
    
    settings = get_settings()
    
    if settings.DATABASE_URL.startswith("sqlite"):
        database_url = settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
    else:
        database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    engine = create_async_engine(database_url)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        yield session

@router.post("/", response_model=ItemResponse, status_code=201)
async def create_item(
    item: ItemCreate,
    db: AsyncSession = Depends(get_database)
):
    """Create a new item"""
    try:
        service = ItemService(db)
        return await service.create_item(item)
    except Exception as e:
        logger.error(f"Failed to create item: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=List[ItemResponse])
async def get_items(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of items to return"),
    db: AsyncSession = Depends(get_database)
):
    """Get all items with pagination"""
    try:
        service = ItemService(db)
        return await service.get_items(skip=skip, limit=limit)
    except Exception as e:
        logger.error(f"Failed to retrieve items: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(
    item_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Get a specific item by ID"""
    try:
        service = ItemService(db)
        item = await service.get_item(item_id)
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve item {item_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: int,
    item: ItemUpdate,
    db: AsyncSession = Depends(get_database)
):
    """Update an existing item"""
    try:
        service = ItemService(db)
        updated_item = await service.update_item(item_id, item)
        if not updated_item:
            raise HTTPException(status_code=404, detail="Item not found")
        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update item {item_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{item_id}", status_code=204)
async def delete_item(
    item_id: int,
    db: AsyncSession = Depends(get_database)
):
    """Delete an item"""
    try:
        service = ItemService(db)
        deleted = await service.delete_item(item_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Item not found")
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete item {item_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")