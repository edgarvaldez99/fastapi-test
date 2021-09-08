from sqlalchemy import BigInteger, Column, String  # type: ignore

from app.database import Base


class AuditRequest(Base):
    """
    Defines the audit request model
    """

    id = Column(BigInteger, primary_key=True)
    ip = Column(String)
    url = Column(String)

    def __repr__(self) -> str:
        return f"<AuditRequest {self.id}>"
