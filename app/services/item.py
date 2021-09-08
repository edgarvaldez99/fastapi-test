from fastapi import HTTPException
from sqlalchemy.orm import Session  # type: ignore

from app import repositories


def get_item_by_name(name: str, db: Session):
    item = repositories.item.get_item_by_name(db=db, name=name)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
