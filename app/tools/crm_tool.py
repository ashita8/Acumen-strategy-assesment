from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.models.crm_profile_model import (
    CRMProfile
)


async def fetch_crm_profile(
    client_id: str
):

    db: Session = SessionLocal()

    try:

        crm_profile = (
            db.query(CRMProfile)
            .filter(
                CRMProfile.client_id ==
                client_id
            )
            .first()
        )

        if not crm_profile:

            return None

        return {
            "client_segment":
                crm_profile.client_segment,

            "risk_appetite":
                crm_profile.risk_appetite,

            "investment_goal":
                crm_profile.investment_goal,

            "relationship_years":
                crm_profile.relationship_years,

            "credit_score":
                crm_profile.credit_score,

            "advisor_notes":
                crm_profile.advisor_notes
        }

    finally:

        db.close()