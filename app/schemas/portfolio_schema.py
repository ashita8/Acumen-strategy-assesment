from pydantic import BaseModel
from typing import List


class PortfolioAnalysisSchema(BaseModel):

    investment_profile: str

    liquidity_assessment: str

    debt_exposure: str

    diversification_score: str

    overall_risk_level: str

    savings_ratio: float

    debt_to_income_ratio: float

    key_insights: List[str]