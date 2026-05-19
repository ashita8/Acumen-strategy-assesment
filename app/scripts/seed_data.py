from app.core.database import SessionLocal
from app.core.init_db import init_db

from app.services.faker_service import (
    generate_mock_client
)

from app.services.client_service import (
    create_client
)

TOTAL_CLIENTS = 10

async def seed_clients():

    init_db()

    db = SessionLocal()

    try:

        for _ in range(TOTAL_CLIENTS):

            payload = generate_mock_client()

            client = await create_client(
                db,
                payload
            )

            print(
                f"Created client: "
                f"{client.client_id}"
            )

    finally:

        db.close()


if __name__ == "__main__":

    import asyncio

    asyncio.run(
        seed_clients()
    )