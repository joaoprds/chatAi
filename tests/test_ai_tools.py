from app.ai.tools import get_product_stock
from app.ai.schemas import GetProductStockInput


def test_get_product_stock(db_session):
    params = GetProductStockInput(
        company_id=1,
        sku="PROD-001"
    )

    result = get_product_stock(db_session, params)

    assert result["success"] is True
    assert result["product"]["sku"] == "PROD-001"
    assert result["product"]["stock_quantity"] == 100