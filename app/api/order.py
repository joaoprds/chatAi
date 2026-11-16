from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import OrderService


router = APIRouter(
    prefix="/companies/{company_id}/orders",
    tags=["Orders"],
)

service = OrderService()


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    company_id: int,
    payload: OrderCreate,
    db: Session = Depends(get_db),
):
    return service.create(
        db,
        company_id,
        payload.customer_id,
        payload.items,
        payload.due_date,
    )


@router.get("", response_model=list[OrderResponse])
def list_orders(
    company_id: int,
    db: Session = Depends(get_db),
):
    return service.list_by_company(db, company_id)