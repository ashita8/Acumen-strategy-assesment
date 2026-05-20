def format_final_response(state):

    return {

        "client_id": state.get(
            "client_id"
        ),

        "portfolio_analysis": state.get(
            "portfolio_analysis",
            {}
        ),

        "risk_assessment": state.get(
            "risk_assessment",
            {}
        ),

        "anomalies": state.get(
            "anomalies",
            []
        ),

        "advisory_report": state.get(
            "advisory_report",
            {}
        ),

        "execution_summary": {

            "next_step": state.get(
                "next_step"
            ),

            "workflow_logs": state.get(
                "execution_logs",
                []
            ),

            "errors": state.get(
                "errors",
                []
            )
        }
    }