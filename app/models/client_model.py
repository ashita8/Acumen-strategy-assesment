from sqlalchemy import (
    Column,
    String,
    Float
)

from app.core.database import Base


class Client(Base):

    __tablename__ = "clients"

    client_id = Column(
        String,
        primary_key=True
    )

    name = Column(
        String
    )

    monthly_income = Column(
        Float
    )

    monthly_expenses = Column(
        Float
    )

    savings_balance = Column(
        Float
    )