from sqlalchemy import BigInteger, Column, Integer, String  # type: ignore

from app.audits.audit_mixin import AuditMixin
from app.database import Base


class Item(AuditMixin, Base):
    """
    Defines the items model
    """

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    def __repr__(self) -> str:
        return f"<Item {self.name}>"
