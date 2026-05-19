from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.models.client_model import Client
from app.models.transaction_model import Transaction
from app.models.investments_model import Investment


async def fetch_client_financial_data(
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

            return None

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

        return {
            "client_profile": {
                "client_id": client.client_id,
                "name": client.name,
                "monthly_income":
                    client.monthly_income,
                "monthly_expenses":
                    client.monthly_expenses,
                "savings_balance":
                    client.savings_balance
            },

            "transactions": [
                {
                    "transaction_id":
                        transaction.transaction_id,

                    "amount":
                        transaction.amount,

                    "category":
                        transaction.category,

                    "transaction_type":
                        transaction.transaction_type
                }

                for transaction in transactions
            ],

            "investments": [
                {
                    "asset_name":
                        investment.asset_name,

                    "asset_type":
                        investment.asset_type,

                    "current_value":
                        investment.current_value
                }

                for investment in investments
            ]
        }

    finally:

        db.close()