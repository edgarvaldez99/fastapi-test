from fastapi import APIRouter

from app.endpoints import item, login, user

api = APIRouter()
api.include_router(login.api, prefix="/login", tags=["login"])
api.include_router(user.api, prefix="/user", tags=["user"])
api.include_router(item.api, prefix="/item", tags=["item"])
