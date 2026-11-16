from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.company import CompanyCreate, CompanyResponse
from app.services.company_service import CompanyService


router = APIRouter(prefix="/companies", tags=["Companies"])

service = CompanyService()


@router.post(
    "",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_company(
    payload: CompanyCreate,
    db: Session = Depends(get_db),
):
    return service.create(
        db,
        payload.name,
        payload.document,
    )


@router.get("", response_model=list[CompanyResponse])
def list_companies(db: Session = Depends(get_db)):
    return service.list_all(db)


@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
):
    return service.get_by_id(db, company_id)