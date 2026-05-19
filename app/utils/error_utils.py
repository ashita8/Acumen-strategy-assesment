def append_workflow_error(
    state,
    agent_name: str,
    error_message: str
):

    state["errors"].append({
        "agent": agent_name,
        "error": error_message
    })

    state["execution_logs"].append(
        f"{agent_name} failed: {error_message}"
    )

    return state