from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.company_repository import CompanyRepository
from app.repositories.customer_repository import CustomerRepository


class CustomerService:

    def __init__(self):
        self.customer_repository = CustomerRepository()
        self.company_repository = CompanyRepository()

    def create(
        self,
        db: Session,
        company_id: int,
        name: str,
        email: str,
    ):
        company = self.company_repository.get_by_id(db, company_id)

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found",
            )

        return self.customer_repository.create(
            db,
            company_id,
            name,
            email,
        )

    def list_by_company(self, db: Session, company_id: int):
        company = self.company_repository.get_by_id(db, company_id)

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found",
            )

        return self.customer_repository.list_by_company(
            db,
            company_id,
        )