from typing import TypedDict, Dict, List


class AgentState(TypedDict):
    client_data: Dict
    analysis: Dict
    logs: List[str]

class WorkflowState(TypedDict):

    client_id: str

    client_profile: Dict

    transactions: List[Dict]

    investments: List[Dict]

    portfolio_analysis: Dict

    risk_assessment: Dict

    anomalies: List[Dict]

    advisory_report: Dict

    next_step: str

    execution_logs: List[str]

    crm_profile: Dict

    market_context: Dict

    errors: List[Dict]