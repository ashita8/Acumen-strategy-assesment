from app.core.database import Base, engine
# from app.models.client_model import Client
from app.models.client_memory_model import ClientMemory
from app.models.transaction_model import Transaction
from app.models.investments_model import Investment
from app.models.crm_profile_model import CRMProfile

def init_db():

    Base.metadata.create_all(
        bind=engine
    )