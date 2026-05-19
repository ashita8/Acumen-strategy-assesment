from typing import TypedDict, Dict, List


class AgentState(TypedDict):
    client_data: Dict
    analysis: Dict
    logs: List[str]