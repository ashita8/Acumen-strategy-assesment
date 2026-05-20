from sqlalchemy import text

from app.core.database import engine


class MemoryService:

    @staticmethod
    async def save_memory(

        client_id,
        memory_type,
        memory_summary
    ):

        query = text(
            """
            INSERT INTO client_memory (
                client_id,
                memory_type,
                memory_summary
            )
            VALUES (
                :client_id,
                :memory_type,
                :memory_summary
            )
            """
        )

        with engine.begin() as conn:

            conn.execute(
                query,
                {
                    "client_id": client_id,
                    "memory_type": memory_type,
                    "memory_summary": memory_summary
                }
            )

    @staticmethod
    async def get_memories(client_id):

        query = text(
            """
            SELECT memory_summary
            FROM client_memory
            WHERE client_id = :client_id
            ORDER BY created_at DESC
            LIMIT 5
            """
        )

        with engine.begin() as conn:

            result = conn.execute(
                query,
                {
                    "client_id": client_id
                }
            )

            return [
                row[0]
                for row in result.fetchall()
            ]