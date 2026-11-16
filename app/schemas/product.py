from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    sku: str = Field(min_length=2, max_length=50)
    name: str = Field(min_length=2, max_length=150)

    price: Decimal = Field(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )

    stock_quantity: int = Field(ge=0)


class ProductResponse(BaseModel):
    id: int
    company_id: int
    sku: str
    name: str
    price: Decimal
    stock_quantity: int

    model_config = ConfigDict(from_attributes=True)