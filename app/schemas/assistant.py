from pydantic import BaseModel, Field


class AssistantRequest(BaseModel):
    message: str = Field(min_length=1, max_length=5000)
    conversation_id: int | None = None


class AssistantResponse(BaseModel):
    conversation_id: int
    answer: str