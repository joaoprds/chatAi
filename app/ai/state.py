from typing import TypedDict
from sqlalchemy.orm import Session


class AgentState(TypedDict):
    company_id: int
    input_items: list[dict]
    pending_calls: list[dict]
    answer: str
    tool_rounds: int


class AgentContext(TypedDict):
    db: Session