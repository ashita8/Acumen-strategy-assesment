from sqlalchemy.orm import Session

from app.models.client_model import Client
from app.models.transaction_model import Transaction
from app.models.investments_model import Investment

from app.core.database import SessionLocal

from app.services.crm_service import (
    get_crm_profile
)

from app.services.market_service import (
    get_market_context
)


# =========================================================
# Create Client
# =========================================================

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


# =========================================================
# Fetch Full Client Workflow Context
# =========================================================

async def fetch_client_data(
    client_id: str
):

    db: Session = SessionLocal()

    try:

        client = (
            db.query(Client)
            .filter(
                Client.client_id == client_id
            )
            .first()
        )

        if not client:

            raise Exception(
                f"Client not found: {client_id}"
            )

        transactions = (
            db.query(Transaction)
            .filter(
                Transaction.client_id == client_id
            )
            .all()
        )

        investments = (
            db.query(Investment)
            .filter(
                Investment.client_id == client_id
            )
            .all()
        )

        crm_profile = await get_crm_profile(
            client_id
        )

        market_context = (
            await get_market_context()
        )

        return {

            "client_profile": {

                "client_id": str(
                    client.client_id
                ),

                "name": client.name,

                "monthly_income": (
                    client.monthly_income
                ),

                "monthly_expenses": (
                    client.monthly_expenses
                ),

                "savings_balance": (
                    client.savings_balance
                )
            },

            "transactions": [

                {
                    "transaction_id": str(
                        tx.transaction_id
                    ),

                    "amount": tx.amount,

                    "category": tx.category,

                    "transaction_type": (
                        tx.transaction_type
                    )
                }

                for tx in transactions
            ],

            "investments": [

                {
                    "asset_name": (
                        inv.asset_name
                    ),

                    "asset_type": (
                        inv.asset_type
                    ),

                    "current_value": (
                        inv.current_value
                    )
                }

                for inv in investments
            ],

            "crm_profile": crm_profile,

            "market_context": market_context
        }

    finally:

        db.close()