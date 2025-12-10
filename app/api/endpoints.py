from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import date

from app.models import (
    CustomerCreate, Response,
    OrderCreate,
    PaymentCreate,
    ApiResponse
)
from app.services.retailcrm_service import retailcrm_service
from app.utils.helpers import (
    format_date_for_api, prepare_customer_data,
    prepare_order_data, prepare_payment_data
)

router = APIRouter(prefix="/api/v1", tags=["RetailCRM Integration"])


# 1. Получение списка клиентов
@router.get("/customers", response_model=ApiResponse)
def get_customers(
        name: Optional[str] = Query(None, description="Фильтр по имени клиента"),
        email: Optional[str] = Query(None, description="Фильтр по email"),
        created_from: Optional[date] = Query(None, description="Фильтр по дате регистрации"),
        created_to: Optional[date] = Query(None, description="Фильтр по дате регистрации"),
        limit: int = Query(20, ge=1, le=100, description="Количество записей"),
        page: int = Query(1, ge=1, description="Номер страницы")
):
    """Получение списка клиентов из RetailCRM с фильтрацией"""
    try:
        created_from_str = format_date_for_api(created_from)
        created_to_str = format_date_for_api(created_to)

        response = retailcrm_service.get_customers(
            name=name,
            email=email,
            created_from=created_from_str,
            created_to=created_to_str,
            limit=limit,
            page=page
        )

        if response.get("success"):
            customers = response.get("customers", [])
            return {
                "success": True,
                "message": f"Найдено {len(customers)} клиентов",
                "data": {"customers": customers},
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка RetailCRM: {response.get('errorMsg', 'Unknown error')}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 2. Создание нового клиента
@router.post("/customers", response_model=Response)
def create_customer(customer: CustomerCreate):
    """Создание нового клиента в RetailCRM"""
    try:
        customer_data = prepare_customer_data(customer.model_dump())

        response = retailcrm_service.create_customer(customer_data)

        if response.get("success"):
            return response
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка RetailCRM: {response.get('errorMsg', 'Unknown error')}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 3. Получение списка заказов клиента
@router.get("/customers/{customer_id}/orders", response_model=ApiResponse)
def get_customer_orders(
        customer_id: int,
        limit: int = Query(20, ge=1, le=100, description="Количество записей"),
        page: int = Query(1, ge=1, description="Номер страницы")
):
    """Получение списка заказов клиента по его ID"""
    try:
        response = retailcrm_service.get_customer_orders(
            customer_id=customer_id,
            limit=limit,
            page=page
        )

        if response.get("success"):
            orders = response.get("orders", [])
            return ApiResponse(
                success=True,
                message=f"Найдено {len(orders)} заказов",
                data={"orders": orders}
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка RetailCRM: {response.get('errorMsg', 'Unknown error')}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 4. Создание нового заказа
@router.post("/orders", response_model=Response)
def create_order(order: OrderCreate):
    """Создание нового заказа в RetailCRM"""
    try:
        # Подготовка данных заказа
        order_data = prepare_order_data(order.model_dump())

        response = retailcrm_service.create_order(order_data)

        if response.get("success"):
            return response
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка RetailCRM: {response.get('errorMsg', 'Unknown error')}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 5. Создание и привязка платежа к заказу
@router.post("/payments", response_model=Response)
def create_payment(payment: PaymentCreate):
    """Создание платежа и привязка его к заказу"""
    try:
        payment_data = prepare_payment_data(
            order_id=payment.order_id,
            amount=payment.amount,
            payment_type=payment.payment_type,
            comment=payment.comment
        )

        response = retailcrm_service.create_payment(payment_data)

        if response.get("success"):
            return response
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Ошибка RetailCRM: {response.get('errorMsg', 'Unknown error')}"
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
