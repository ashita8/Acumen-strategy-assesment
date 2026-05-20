from pydantic import BaseModel
from typing import Literal


class OrchestratorDecisionSchema(BaseModel):

    next_step: Literal[
        "risk_evaluator",
        "advisory_agent"
    ]

    reasoning: str