from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Customer, Order, OrderItem, Product
from app.repositories.company_repository import CompanyRepository


class OrderService:

    def __init__(self):
        self.company_repository = CompanyRepository()

    def create(
        self,
        db: Session,
        company_id: int,
        customer_id: int,
        items: list,
        due_date=None,
    ):

        try:
            company = self.company_repository.get_by_id(
                db,
                company_id,
            )

            if not company:
                raise HTTPException(
                    status_code=404,
                    detail="Company not found",
                )

            customer = db.scalar(
                select(Customer).where(
                    Customer.id == customer_id,
                    Customer.company_id == company_id,
                )
            )

            if not customer:
                raise HTTPException(
                    status_code=404,
                    detail="Customer not found",
                )

            order_items = []
            total_amount = Decimal("0.00")

            for item in items:

                product = db.scalar(
                    select(Product).where(
                        Product.id == item.product_id,
                        Product.company_id == company_id,
                    )
                )

                if not product:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product {item.product_id} not found",
                    )

                if product.stock_quantity < item.quantity:
                    raise HTTPException(
                        status_code=409,
                        detail=f"Insufficient stock for {product.name}",
                    )

                line_total = product.price * item.quantity

                total_amount += line_total

                order_items.append(
                    OrderItem(
                        product_id=product.id,
                        quantity=item.quantity,
                        unit_price=product.price,
                        line_total=line_total,
                    )
                )

            order = Order(
                company_id=company_id,
                customer_id=customer_id,
                status="pending",
                total_amount=total_amount,
                due_date=due_date,
                items=order_items,
            )

            db.add(order)
            db.commit()

            statement = (
                select(Order)
                .options(selectinload(Order.items))
                .where(Order.id == order.id)
            )

            return db.scalar(statement)

        except Exception:
            db.rollback()
            raise

    def list_by_company(
        self,
        db: Session,
        company_id: int,
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

        statement = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.company_id == company_id)
            .order_by(Order.created_at.desc())
        )

        return list(db.scalars(statement).all())