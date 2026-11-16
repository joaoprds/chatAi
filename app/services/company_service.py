from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.company_repository import CompanyRepository


class CompanyService:

    def __init__(self):
        self.repository = CompanyRepository()

    def create(self, db: Session, name: str, document: str):
        existing = self.repository.get_by_document(db, document)

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Company document already registered",
            )

        return self.repository.create(db, name, document)

    def list_all(self, db: Session):
        return self.repository.list_all(db)

    def get_by_id(self, db: Session, company_id: int):
        company = self.repository.get_by_id(db, company_id)

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found",
            )

        return company