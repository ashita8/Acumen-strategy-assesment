from sqlalchemy import (
    Column,
    String,
    Text,
    Integer,
    DateTime
)

from datetime import datetime

from app.core.database import Base


class ClientMemory(Base):

    __tablename__ = "client_memory"

    id = Column(
        Integer,
        primary_key=True
    )

    client_id = Column(
        String,
        nullable=False
    )

    memory_type = Column(
        String,
        nullable=False
    )

    memory_summary = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )