from datetime import date, datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class OrderItemCreate(BaseModel):
    product_id: int

    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_id: int

    due_date: date | None = None

    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    line_total: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    company_id: int
    customer_id: int

    status: Literal[
        "pending",
        "processing",
        "shipped",
        "delivered",
        "cancelled",
    ]

    total_amount: Decimal
    due_date: date | None
    created_at: datetime
    items: list[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)