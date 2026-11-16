from fastapi import FastAPI

from app.api.companies import router as companies_router
from app.api.customers import router as customers_router
from app.api.products import router as products_router
from app.api.order import router as orders_router
from app.api.assistant import router as assistant_router


app = FastAPI(
    title="Enterprise AI Operations Platform",
    description="AI-powered enterprise operations platform",
    version="0.2.0",
)

app.include_router(companies_router, prefix="/api/v1")
app.include_router(customers_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")
app.include_router(
    assistant_router,
    prefix="/api/v1",
    tags=["AI Assistant"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "application": "enterprise-ai-platform",
        "version": "0.2.0",
    }