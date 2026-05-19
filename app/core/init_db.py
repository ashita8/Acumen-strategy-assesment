from app.core.database import Base, engine
from app.models.client_model import Client


def init_db():

    Base.metadata.create_all(
        bind=engine
    )