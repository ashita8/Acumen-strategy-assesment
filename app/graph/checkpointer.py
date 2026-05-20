from langgraph.checkpoint.postgres.aio import (
    AsyncPostgresSaver
)

from app.core.configs import settings


checkpointer_cm = (
    AsyncPostgresSaver.from_conn_string(
        settings.DATABASE_URL
    )
)

checkpointer = None