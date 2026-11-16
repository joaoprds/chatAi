from pydantic import BaseModel, ConfigDict, Field


class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    document: str = Field(min_length=5, max_length=30)


class CompanyResponse(BaseModel):
    id: int
    name: str
    document: str

    model_config = ConfigDict(from_attributes=True)