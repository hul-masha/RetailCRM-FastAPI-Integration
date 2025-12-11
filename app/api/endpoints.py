from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from datetime import date

from app.models import CustomerCreate, Response, OrderCreate, PaymentCreate, ApiResponse
from app.services.retailcrm_service import retailcrm_service
from app.utils.helpers import (
    format_date_for_api,
    prepare_customer_data,
    prepare_order_data,
    prepare_payment_data,
)

router = APIRouter(prefix="/api/v1", tags=["RetailCRM Integration"])


@router.get("/customers", response_model=ApiResponse)
def get_customers(
    name: Optional[str] = Query(None, description="Filter by customer name"),
    email: Optional[str] = Query(None, description="Filter by customer email"),
    created_from: Optional[date] = Query(
        None, description="Filter by date of creation"
    ),
    created_to: Optional[date] = Query(None, description="Filter by date of creation"),
    limit: int = Query(20, ge=1, le=100, description="Amount of lines"),
    page: int = Query(1, ge=1, description="Page number"),
):
    """List of customers from RetailCRM with filters"""
    try:
        created_from_str = format_date_for_api(created_from)
        created_to_str = format_date_for_api(created_to)

        response = retailcrm_service.get_customers(
            name=name,
            email=email,
            created_from=created_from_str,
            created_to=created_to_str,
            limit=limit,
            page=page,
        )

        if response.get("success"):
            customers = response.get("customers", [])
            return {
                "success": True,
                "message": f"Found {len(customers)} customers",
                "data": {"customers": customers},
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Error RetailCRM: {response.get('errorMsg', 'Unknown error')}",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/customers", response_model=Response)
def create_customer(customer: CustomerCreate):
    """New customer creation in RetailCRM"""
    try:
        customer_data = prepare_customer_data(customer.model_dump())

        response = retailcrm_service.create_customer(customer_data)

        if response.get("success"):
            return response
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Error RetailCRM: {response.get('errorMsg', 'Unknown error')}",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/customers/{customer_id}/orders", response_model=ApiResponse)
def get_customer_orders(
    customer_id: int,
    limit: int = Query(20, ge=1, le=100, description="Amount of lines"),
    page: int = Query(1, ge=1, description="Page number"),
):
    """List of orders by customer ID"""
    try:
        response = retailcrm_service.get_customer_orders(
            customer_id=customer_id, limit=limit, page=page
        )

        if response.get("success"):
            orders = response.get("orders", [])
            return ApiResponse(
                success=True,
                message=f"Found {len(orders)} orders",
                data={"orders": orders},
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Error RetailCRM: {response.get('errorMsg', 'Unknown error')}",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/orders", response_model=Response)
def create_order(order: OrderCreate):
    """New order creation in RetailCRM"""
    try:
        order_data = prepare_order_data(order.model_dump())

        response = retailcrm_service.create_order(order_data)

        if response.get("success"):
            return response
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Error RetailCRM: {response.get('errorMsg', 'Unknown error')}",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/payments", response_model=Response)
def create_payment(payment: PaymentCreate):
    """Payment creation with order attachment"""
    try:
        payment_data = prepare_payment_data(
            order_id=payment.order_id,
            amount=payment.amount,
            payment_type=payment.payment_type,
            comment=payment.comment,
        )

        response = retailcrm_service.create_payment(payment_data)

        if response.get("success"):
            return response
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Error RetailCRM: {response.get('errorMsg', 'Unknown error')}",
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
