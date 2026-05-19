from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.models.client_model import Client

from app.models.crm_profile_model import (
    CRMProfile
)


async def list_clients():

    db: Session = SessionLocal()

    try:

        clients = (
            db.query(
                Client,
                CRMProfile
            )
            .join(
                CRMProfile,
                CRMProfile.client_id ==
                Client.client_id
            )
            .all()
        )

        response = []

        for client, crm in clients:

            response.append({
                "client_id":
                    client.client_id,

                "name":
                    client.name,

                "client_segment":
                    crm.client_segment,

                "risk_appetite":
                    crm.risk_appetite
            })

        return response

    finally:

        db.close()