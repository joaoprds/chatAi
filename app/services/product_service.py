from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.company_repository import CompanyRepository
from app.repositories.product_repository import ProductRepository


class ProductService:

    def __init__(self):
        self.repository = ProductRepository()
        self.company_repository = CompanyRepository()

    def create(
        self,
        db: Session,
        company_id: int,
        sku: str,
        name: str,
        price,
        stock_quantity: int,
    ):

        company = self.company_repository.get_by_id(
            db,
            company_id,
        )

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found",
            )

        existing = self.repository.get_by_sku(
            db,
            company_id,
            sku,
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Product SKU already registered",
            )

        try:
            return self.repository.create(
                db,
                company_id,
                sku,
                name,
                price,
                stock_quantity,
            )

        except IntegrityError:
            db.rollback()

            raise HTTPException(
                status_code=409,
                detail="Product SKU already registered",
            )

    def list_by_company(self, db: Session, company_id: int):

        company = self.company_repository.get_by_id(
            db,
            company_id,
        )

        if not company:
            raise HTTPException(
                status_code=404,
                detail="Company not found",
            )

        return self.repository.list_by_company(
            db,
            company_id,
        )