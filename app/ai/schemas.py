from pydantic import BaseModel, Field


class GetProductStockInput(BaseModel):
    sku: str = Field(min_length=1)


class GetCustomerOrdersInput(BaseModel):
    customer_id: int
    limit: int = Field(default=10, ge=1, le=50)