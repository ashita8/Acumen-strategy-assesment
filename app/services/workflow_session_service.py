from sqlalchemy.orm import Session

from app.core.database import (
    SessionLocal
)

from app.models.workflow_session_model import (
    WorkflowSession
)
from app.services.logging_service import (
    logger
)


# =========================================
# Save Workflow Session
# =========================================

def save_workflow_session(

    client_id: str,

    thread_id: str,

    status: str
):

    db: Session = SessionLocal()

    try:

        session = WorkflowSession(

            client_id=client_id,

            thread_id=thread_id,

            status=status
        )

        db.add(session)

        db.commit()

    finally:

        db.close()


# =========================================
# Fetch Latest Interrupted Session
# =========================================

def get_latest_interrupted_thread_id(
    client_id: str
):

    db: Session = SessionLocal()

    try:

        session = (

            db.query(WorkflowSession)

            .filter(

                WorkflowSession.client_id
                == client_id,

                WorkflowSession.status
                == "interrupted"
            )

            .order_by(
                WorkflowSession.created_at.desc()
            )

            .first()
        )

        if not session:

            return None

        return session.thread_id

    finally:

        db.close()

# =========================================
# Update Workflow Status
# =========================================

def update_workflow_status(

    thread_id: str,

    status: str
):

    db: Session = SessionLocal()

    try:

        session = (

            db.query(WorkflowSession)

            .filter(
                WorkflowSession.thread_id
                == thread_id
            )

            .first()
        )

        if not session:

            return

        session.status = status

        db.commit()
        logger.info(
        f"Updating workflow status "
        f"thread_id={thread_id} "
        f"status={status}"
        )

    finally:

        db.close()