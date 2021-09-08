from typing import List

from sqlalchemy.orm import Session  # type: ignore

from app.models.item import Item
from app.schemas.item import ItemBase
from app.schemas.user import User


def get_item_by_name(db: Session, name: str) -> Item:
    return db.query(Item).filter(Item.name == name).first()


def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
    return db.query(Item).offset(skip).limit(limit).all()


def create_item(db: Session, *, item: ItemBase):
    db_item = Item(**item.dict())  # type: ignore
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
