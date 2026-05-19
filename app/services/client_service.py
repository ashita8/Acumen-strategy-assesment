from sqlalchemy.orm import Session

from app.models.client_model import Client


async def create_client(
    db: Session,
    payload: dict
):

    client = Client(**payload)

    db.add(client)

    db.commit()

    db.refresh(client)

    return client