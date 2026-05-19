import random
import uuid

from faker import Faker

fake = Faker()

CATEGORIES = [
    "shopping",
    "food",
    "travel",
    "healthcare",
    "salary",
    "investment"
]

ASSET_TYPES = [
    "equity",
    "mutual_fund",
    "bond",
    "crypto"
]


def generate_mock_client():

    client_id = str(uuid.uuid4())

    income = random.randint(
        80000,
        250000
    )

    expenses = random.randint(
        30000,
        150000
    )

    transactions = []

    for _ in range(random.randint(5, 15)):

        transactions.append({
            "transaction_id": str(uuid.uuid4()),
            "amount": random.randint(500, 50000),
            "category": random.choice(CATEGORIES),
            "transaction_type": random.choice(
                ["credit", "debit"]
            )
        })

    investments = []

    for _ in range(random.randint(2, 5)):

        investments.append({
            "asset_name": fake.company(),
            "asset_type": random.choice(ASSET_TYPES),
            "current_value": random.randint(
                10000,
                300000
            )
        })

    return {
        "client": {
            "client_id": client_id,
            "name": fake.name(),
            "monthly_income": income,
            "monthly_expenses": expenses,
            "savings_balance": random.randint(
                100000,
                1000000
            )
        },
        "transactions": transactions,
        "investments": investments
    }