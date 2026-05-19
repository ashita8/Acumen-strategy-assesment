import asyncio

from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.models.client_model import Client
from app.models.crm_profile_model import CRMProfile

from app.services.faker_service import (
    generate_crm_profile
)


async def seed_crm_profiles():

    db: Session = SessionLocal()

    try:

        clients = db.query(Client).all()

        for client in clients:

            existing_profile = (
                db.query(CRMProfile)
                .filter(
                    CRMProfile.client_id ==
                    client.client_id
                )
                .first()
            )

            if existing_profile:
                continue

            crm_data = generate_crm_profile(
                client.client_id
            )

            crm_profile = CRMProfile(
                **crm_data
            )

            db.add(crm_profile)

        db.commit()

        print(
            "CRM profiles seeded successfully"
        )

    finally:

        db.close()


if __name__ == "__main__":

    asyncio.run(
        seed_crm_profiles()
    )