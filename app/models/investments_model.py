from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    ForeignKey
)

from app.core.database import Base


class Investment(Base):

    __tablename__ = "investments"

    id = Column(Integer, primary_key=True)

    client_id = Column(
        String,
        ForeignKey("clients.client_id")
    )

    asset_name = Column(String)

    asset_type = Column(String)

    current_value = Column(Float)