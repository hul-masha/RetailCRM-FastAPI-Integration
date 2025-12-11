from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router

app = FastAPI(
    title="RetailCRM Integration API",
    description="Integration with RetailCRM API for customer and order management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "RetailCRM Integration API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "customers": {
                "GET": "/api/v1/customers - Get list of customers",
                "POST": "/api/v1/customers - Create customer",
            },
            "orders": {
                "GET": "/api/v1/customers/{id}/orders - Get list of orders",
                "POST": "/api/v1/orders - Create order",
            },
            "payments": {"POST": "/api/v1/payments - Create payment"},
        },
    }


@app.get("/health")
def health_check():
    """App health check endpoint"""
    return {"status": "healthy"}
