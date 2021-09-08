from sqlalchemy import Boolean, Column, Integer, String  # type: ignore

from app.database.base import Base


class User(Base):
    """
    Defines the user model
    """

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    token = Column(String, unique=True)

    def __repr__(self) -> str:
        return f"<User {self.full_name}>"
