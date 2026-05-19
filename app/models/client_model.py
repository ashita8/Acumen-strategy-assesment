from sqlalchemy import (
    Column,
    String,
    Float,
    Integer
)

from app.core.database import Base


class Client(Base):

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)

    client_id = Column(
        String,
        unique=True,
        nullable=False
    )

    name = Column(String, nullable=False)

    monthly_income = Column(Float)

    monthly_expenses = Column(Float)

    savings_balance = Column(Float)