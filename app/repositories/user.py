import datetime
from typing import Optional

from sqlalchemy.orm import Session  # type: ignore
from sqlalchemy.sql.sqltypes import BigInteger  # type: ignore

from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_md5_hash_hexdigest, get_password_hash


def create(db: Session, *, obj_in: UserCreate) -> User:
    created_at = datetime.datetime.now()
    string_to_hash = "%s-%s-%s" % (created_at, obj_in.email, obj_in.full_name)
    token = get_md5_hash_hexdigest(string_to_hash)
    password = obj_in.password if obj_in.password else ""
    db_obj = User(
        email=obj_in.email,
        token=token,
        hashed_password=get_password_hash(password),
        full_name=obj_in.full_name,
        is_superuser=obj_in.is_superuser,
    )  # type: ignore
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get(db: Session, id: BigInteger) -> Optional[User]:
    return db.query(User).filter(User.id == id).first()


def get_by_email(db: Session, *, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()
