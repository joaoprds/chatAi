from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import Product, Customer, Order
from app.ai.schemas import (
    GetProductStockInput,
    GetCustomerOrdersInput,
)


def get_product_stock(
    db: Session,
    company_id: int,
    params: GetProductStockInput,
) -> dict:

    product = db.scalar(
        select(Product).where(
            Product.company_id == company_id,
            Product.sku == params.sku
        )
    )

    if not product:
        return {
            "success": False,
            "message": "Product not found."
        }

    return {
        "success": True,
        "product": {
            "id": product.id,
            "sku": product.sku,
            "name": product.name,
            "stock_quantity": product.stock_quantity,
            "price": str(product.price)
        }
    }


def get_customer_orders(
    db: Session,
    company_id: int,
    params: GetCustomerOrdersInput
) -> dict:

    customer = db.scalar(
        select(Customer).where(
            Customer.id == params.customer_id,
            Customer.company_id == company_id
        )
    )

    if not customer:
        return {
            "success": False,
            "message": "Customer not found."
        }

    orders = db.scalars(
        select(Order)
        .options(selectinload(Order.items))
        .where(
            Order.company_id == company_id,
            Order.customer_id == params.customer_id
        )
        .order_by(Order.created_at.desc())
        .limit(params.limit)
    ).all()

    return {
        "success": True,
        "customer": {
            "id": customer.id,
            "name": customer.name
        },
        "orders": [
            {
                "id": order.id,
                "status": order.status,
                "total_amount": str(order.total_amount),
                "created_at": order.created_at.isoformat(),
                "items": [
                    {
                        "product_id": item.product_id,
                        "quantity": item.quantity,
                        "unit_price": str(item.unit_price),
                        "line_total": str(item.line_total)
                    }
                    for item in order.items
                ]
            }
            for order in orders
        ]
    }