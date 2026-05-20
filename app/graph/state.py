from typing import TypedDict, Dict, List, Any


from typing import TypedDict
from typing import Dict
from typing import Any
from typing import List
from typing import Optional


class AgentState(TypedDict):

    client_id: str

    client_profile: Dict[str, Any]

    transactions: List[Dict[str, Any]]

    investments: List[Dict[str, Any]]

    portfolio_analysis: Dict[str, Any]

    risk_assessment: Dict[str, Any]

    anomalies: List[Dict[str, Any]]

    advisory_report: Any

    next_step: Optional[str]

    execution_logs: List[str]

    crm_profile: Dict[str, Any]

    market_context: Dict[str, Any]

    errors: List[str]

    human_review_decision: Dict[str, Any]

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

    human_review_decision: Dict[str, Any]

    errors: List[Dict]