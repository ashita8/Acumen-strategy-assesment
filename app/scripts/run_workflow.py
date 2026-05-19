import asyncio

from sqlalchemy.orm import Session

from app.core.database import SessionLocal

from app.models.client_model import Client

from app.graph.orchestrator import (
    build_workflow
)


async def run():

    db: Session = SessionLocal()

    try:

        client = db.query(Client).first()

        workflow = build_workflow()

        initial_state = {
            "client_id": client.client_id,

            "client_profile": {},

            "transactions": [],

            "investments": [],

            "portfolio_analysis": {},

            "risk_assessment": {},

            "anomalies": [],

            "advisory_report": {},

            "execution_logs": []
        }

        result = await workflow.ainvoke(
            initial_state
        )

        print("\nFINAL RESULT\n")

        print(result)

    finally:

        db.close()


if __name__ == "__main__":

    asyncio.run(run())