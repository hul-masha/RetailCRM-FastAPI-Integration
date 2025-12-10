from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router

app = FastAPI(
    title="RetailCRM Integration API",
    description="Интеграция с RetailCRM API для управления клиентами и заказами",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root():
    """Корневой эндпоинт"""
    return {
        "message": "RetailCRM Integration API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "customers": {
                "GET": "/api/v1/customers - Получение списка клиентов",
                "POST": "/api/v1/customers - Создание клиента"
            },
            "orders": {
                "GET": "/api/v1/customers/{id}/orders - Заказы клиента",
                "POST": "/api/v1/orders - Создание заказа"
            },
            "payments": {
                "POST": "/api/v1/payments - Создание платежа"
            }
        }
    }


@app.get("/health")
def health_check():
    """Проверка здоровья приложения"""
    return {"status": "healthy"}
