# debe importarse para que sqlalchemy pueda detectar y crear las tablas
from app.database import Base  # noqa

from .item import Item  # noqa
from .user import User  # noqa
