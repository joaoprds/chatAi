from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Customer


class CustomerRepository:

    def create(
        self,
        db: Session,
        company_id: int,
        name: str,
        email: str,
    ) -> Customer:

        customer = Customer(
            company_id=company_id,
            name=name,
            email=email,
        )

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer

    def get_by_id(
        self,
        db: Session,
        company_id: int,
        customer_id: int,
    ):
        statement = select(Customer).where(
            Customer.id == customer_id,
            Customer.company_id == company_id,
        )

        return db.scalar(statement)

    def list_by_company(self, db: Session, company_id: int):
        statement = (
            select(Customer)
            .where(Customer.company_id == company_id)
            .order_by(Customer.id)
        )

        return list(db.scalars(statement).all())