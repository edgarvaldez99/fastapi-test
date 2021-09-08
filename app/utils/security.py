import hashlib

from passlib.context import CryptContext  # type: ignore

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_md5_hash_hexdigest(to_hash: str) -> str:
    return hashlib.md5(to_hash.encode()).hexdigest()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
