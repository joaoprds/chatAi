from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import ProductService


router = APIRouter(
    prefix="/companies/{company_id}/products",
    tags=["Products"],
)

service = ProductService()


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_product(
    company_id: int,
    payload: ProductCreate,
    db: Session = Depends(get_db),
):
    return service.create(
        db,
        company_id,
        payload.sku,
        payload.name,
        payload.price,
        payload.stock_quantity,
    )


@router.get("", response_model=list[ProductResponse])
def list_products(
    company_id: int,
    db: Session = Depends(get_db),
):
    return service.list_by_company(db, company_id)