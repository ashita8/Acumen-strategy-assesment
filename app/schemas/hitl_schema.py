from pydantic import BaseModel
from typing import Optional


class HITLResponseSchema(BaseModel):

    approved: Optional[bool] = None

    advisor_notes: Optional[str] = None