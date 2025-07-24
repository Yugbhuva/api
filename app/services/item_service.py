from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import logging

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate

logger = logging.getLogger("fastapi_app")

class ItemService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_item(self, item_data: ItemCreate) -> Item:
        """Create a new item"""
        try:
            db_item = Item(**item_data.model_dump())
            self.db.add(db_item)
            await self.db.commit()
            await self.db.refresh(db_item)
            logger.info(f"Created item: {db_item.name} (ID: {db_item.id})")
            return db_item
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error creating item: {str(e)}")
            raise
    
    async def get_item(self, item_id: int) -> Optional[Item]:
        """Get item by ID"""
        try:
            result = await self.db.execute(select(Item).where(Item.id == item_id))
            item = result.scalar_one_or_none()
            if item:
                logger.debug(f"Retrieved item: {item.name} (ID: {item.id})")
            return item
        except Exception as e:
            logger.error(f"Error retrieving item {item_id}: {str(e)}")
            raise
    
    async def get_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """Get all items with pagination"""
        try:
            result = await self.db.execute(
                select(Item).offset(skip).limit(limit)
            )
            items = result.scalars().all()
            logger.debug(f"Retrieved {len(items)} items")
            return list(items)
        except Exception as e:
            logger.error(f"Error retrieving items: {str(e)}")
            raise
    
    async def update_item(self, item_id: int, item_data: ItemUpdate) -> Optional[Item]:
        """Update an existing item"""
        try:
            result = await self.db.execute(select(Item).where(Item.id == item_id))
            db_item = result.scalar_one_or_none()
            
            if not db_item:
                return None
            
            # Update only provided fields
            update_data = item_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_item, field, value)
            
            await self.db.commit()
            await self.db.refresh(db_item)
            logger.info(f"Updated item: {db_item.name} (ID: {db_item.id})")
            return db_item
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error updating item {item_id}: {str(e)}")
            raise
    
    async def delete_item(self, item_id: int) -> bool:
        """Delete an item"""
        try:
            result = await self.db.execute(select(Item).where(Item.id == item_id))
            db_item = result.scalar_one_or_none()
            
            if not db_item:
                return False
            
            await self.db.delete(db_item)
            await self.db.commit()
            logger.info(f"Deleted item: {db_item.name} (ID: {db_item.id})")
            return True
        except Exception as e:
            await self.db.rollback()
            logger.error(f"Error deleting item {item_id}: {str(e)}")
            raise