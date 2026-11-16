from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Product


class ProductRepository:

    def create(
        self,
        db: Session,
        company_id: int,
        sku: str,
        name: str,
        price,
        stock_quantity: int,
    ) -> Product:

        product = Product(
            company_id=company_id,
            sku=sku,
            name=name,
            price=price,
            stock_quantity=stock_quantity,
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    def get_by_sku(
        self,
        db: Session,
        company_id: int,
        sku: str,
    ):
        statement = select(Product).where(
            Product.company_id == company_id,
            Product.sku == sku,
        )

        return db.scalar(statement)

    def get_by_id(
        self,
        db: Session,
        company_id: int,
        product_id: int,
    ):
        statement = select(Product).where(
            Product.id == product_id,
            Product.company_id == company_id,
        )

        return db.scalar(statement)

    def list_by_company(
        self,
        db: Session,
        company_id: int,
    ):
        statement = (
            select(Product)
            .where(Product.company_id == company_id)
            .order_by(Product.id)
        )

        return list(db.scalars(statement).all())