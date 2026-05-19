from pydantic import BaseModel
from typing import List


class Transaction(BaseModel):
    transaction_id: str
    amount: float
    category: str
    type: str


class Investment(BaseModel):
    asset_name: str
    asset_type: str
    current_value: float


class ClientFinancialProfile(BaseModel):
    client_id: str
    name: str

    monthly_income: float
    monthly_expenses: float
    savings_balance: float

    transactions: List[Transaction]
    investments: List[Investment]