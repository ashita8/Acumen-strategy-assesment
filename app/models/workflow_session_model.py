from sqlalchemy import (
    Column,
    String,
    DateTime
)

from datetime import datetime

from app.core.database import Base


class WorkflowSession(Base):

    __tablename__ = (
        "workflow_sessions"
    )

    thread_id = Column(
        String,
        primary_key=True
    )

    client_id = Column(
        String,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    