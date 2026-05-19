from app.services.logging_service import logger


async def anomaly_detector_agent(state):

    logger.info(
        "Running anomaly detection"
    )

    anomalies = []

    transactions = state["transactions"]

    if transactions:

        average_transaction = (
            sum(
                transaction["amount"]
                for transaction in transactions
            ) / len(transactions)
        )

        for transaction in transactions:

            if (
                transaction["amount"] >
                average_transaction * 3
            ):

                anomalies.append({
                    "transaction_id":
                    transaction["transaction_id"],
                    "reason":
                    "Unusually high transaction"
                })

    state["anomalies"] = anomalies

    state["execution_logs"].append(
        "Anomaly detection completed"
    )

    return state