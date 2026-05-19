from sqlalchemy.orm import Session

from app.models.client_model import Client
from app.models.transaction_model import Transaction
from app.models.investments_model import Investment


async def create_client(
    db: Session,
    payload: dict
):

    client_payload = payload["client"]

    client = Client(**client_payload)

    db.add(client)

    for transaction_data in payload["transactions"]:

        transaction = Transaction(
            client_id=client.client_id,
            **transaction_data
        )

        db.add(transaction)

    for investment_data in payload["investments"]:

        investment = Investment(
            client_id=client.client_id,
            **investment_data
        )

        db.add(investment)

    db.commit()

    db.refresh(client)

    return client