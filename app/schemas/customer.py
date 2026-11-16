from pydantic import BaseModel, ConfigDict, Field


class CustomerCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    email: str = Field(min_length=5, max_length=255)


class CustomerResponse(BaseModel):
    id: int
    company_id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)