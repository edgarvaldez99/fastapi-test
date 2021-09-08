from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session  # type: ignore

from app import models, repositories, schemas, services
from app.dependencies import get_current_user, get_db_session

api = APIRouter()


@api.get("/", response_model=List[schemas.item.ItemBase])
async def read_items(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)  # noqa: B008
):
    return repositories.item.get_items(db=db, skip=skip, limit=limit)


@api.get("/{name}", response_model=schemas.item.ItemBase)
async def read_item(name: str, db: Session = Depends(get_db_session)):  # noqa: B008
    return services.item.get_item_by_name(db=db, name=name)


@api.post("/", response_model=schemas.item.ItemBase)
async def add_new_item(
    item: schemas.item.ItemBase,
    db: Session = Depends(get_db_session),  # noqa: B008
    current_user: models.User = Depends(get_current_user),  # noqa: B008
):
    return repositories.item.create_item(db=db, item=item, current_user=current_user)
