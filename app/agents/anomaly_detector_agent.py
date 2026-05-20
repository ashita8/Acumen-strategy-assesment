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
            )

            / len(transactions)
        )

        for transaction in transactions:

            if (
                transaction["amount"]
                > average_transaction * 3
            ):

                anomalies.append({

                    "transaction_id":
                        transaction["transaction_id"],

                    "reason":
                        "Unusually high transaction"
                })

    state["anomalies"] = anomalies

    # Conditional Routing

    if anomalies:

        state["next_step"] = (
            "human_review"
        )

        state["execution_logs"].append(
            "Anomalies detected. "
            "Routing to human review."
        )

    else:

        state["next_step"] = (
            "advisory_agent"
        )

        state["execution_logs"].append(
            "No anomalies detected. "
            "Routing directly to advisory."
        )

    return state