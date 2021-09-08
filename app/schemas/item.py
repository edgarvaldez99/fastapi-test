from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    price: int

    class Config:
        orm_mode = True
