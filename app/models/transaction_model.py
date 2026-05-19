from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    ForeignKey
)

from app.core.database import Base


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)

    client_id = Column(
        String,
        ForeignKey("clients.client_id")
    )

    transaction_id = Column(
        String,
        unique=True
    )

    amount = Column(Float)

    category = Column(String)

    transaction_type = Column(String)