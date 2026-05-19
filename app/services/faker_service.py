import random

from faker import Faker

fake = Faker()

def generate_mock_client():

    income = random.randint(
        80000,
        250000
    )

    expenses = random.randint(
        30000,
        150000
    )

    return {
        "client_id": fake.uuid4(),
        "name": fake.name(),
        "monthly_income": income,
        "monthly_expenses": expenses,
        "savings_balance": random.randint(
            100000,
            1000000
        )
    }