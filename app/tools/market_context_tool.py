import random


MARKET_SENTIMENTS = [
    "bullish",
    "bearish",
    "volatile",
    "neutral"
]

EQUITY_OUTLOOKS = [
    "positive",
    "negative",
    "uncertain"
]


async def fetch_market_context():

    return {
        "market_sentiment":
            random.choice(
                MARKET_SENTIMENTS
            ),

        "inflation_rate":
            round(
                random.uniform(2.0, 8.0),
                2
            ),

        "interest_rate":
            round(
                random.uniform(3.0, 7.0),
                2
            ),

        "market_volatility":
            random.choice(
                ["low", "medium", "high"]
            ),

        "equity_outlook":
            random.choice(
                EQUITY_OUTLOOKS
            )
    }