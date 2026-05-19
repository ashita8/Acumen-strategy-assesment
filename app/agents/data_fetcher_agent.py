from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.models.client_model import Client
from app.models.transaction_model import Transaction
from app.models.investments_model import Investment

from app.services.logging_service import logger


async def data_fetcher_agent(state):

    logger.info(
        "Fetching client financial data"
    )

    db: Session = SessionLocal()

    try:

        client = (
            db.query(Client)
            .filter(
                Client.client_id ==
                state["client_id"]
            )
            .first()
        )
        
        if not client:
            state["execution_logs"].append(
                "Client not found"
            )

            raise ValueError(
                "Client does not exist"
            )

        transactions = (
            db.query(Transaction)
            .filter(
                Transaction.client_id ==
                state["client_id"]
            )
            .all()
        )

        investments = (
            db.query(Investment)
            .filter(
                Investment.client_id ==
                state["client_id"]
            )
            .all()
        )

        state["client_profile"] = {
            "client_id": client.client_id,
            "name": client.name,
            "monthly_income": client.monthly_income,
            "monthly_expenses": client.monthly_expenses,
            "savings_balance": client.savings_balance
        }

        state["transactions"] = [
            transaction.__dict__
            for transaction in transactions
        ]

        state["investments"] = [
            investment.__dict__
            for investment in investments
        ]

        state["execution_logs"].append(
            "Client financial data fetched"
        )

        return state

    finally:

        db.close()