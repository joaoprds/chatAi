from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Company


class CompanyRepository:

    def create(self, db: Session, name: str, document: str) -> Company:
        company = Company(
            name=name,
            document=document,
        )

        db.add(company)
        db.commit()
        db.refresh(company)

        return company

    def get_by_id(self, db: Session, company_id: int):
        return db.get(Company, company_id)

    def get_by_document(self, db: Session, document: str):
        statement = select(Company).where(
            Company.document == document
        )

        return db.scalar(statement)

    def list_all(self, db: Session):
        statement = select(Company).order_by(Company.id)

        return list(db.scalars(statement).all())