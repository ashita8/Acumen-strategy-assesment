from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from app.core.database import Base


class CRMProfile(Base):

    __tablename__ = "crm_profiles"

    id = Column(Integer, primary_key=True)

    client_id = Column(
        String,
        ForeignKey("clients.client_id"),
        unique=True
    )

    client_segment = Column(String)

    risk_appetite = Column(String)

    investment_goal = Column(String)

    relationship_years = Column(Integer)

    credit_score = Column(Integer)

    advisor_notes = Column(String)