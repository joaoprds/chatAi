from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.customer import CustomerCreate, CustomerResponse
from app.services.customer_service import CustomerService


router = APIRouter(
    prefix="/companies/{company_id}/customers",
    tags=["Customers"],
)

service = CustomerService()


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_customer(
    company_id: int,
    payload: CustomerCreate,
    db: Session = Depends(get_db),
):
    return service.create(
        db,
        company_id,
        payload.name,
        payload.email,
    )


@router.get("", response_model=list[CustomerResponse])
def list_customers(
    company_id: int,
    db: Session = Depends(get_db),
):
    return service.list_by_company(db, company_id)