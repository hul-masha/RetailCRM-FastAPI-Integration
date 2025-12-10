from datetime import date
from typing import Dict, Any, Optional


def format_date_for_api(date_value: Optional[date]) -> Optional[str]:
    """Форматирование даты для API RetailCRM"""
    if date_value:
        return date_value.strftime("%Y-%m-%d")
    return None


def prepare_customer_data(customer: Dict[str, Any]) -> Dict[str, Any]:
    """Подготовка данных клиента для RetailCRM"""
    return {
        "firstName": customer.get("firstName", ""),
        "lastName": customer.get("lastName"),
        "email": customer.get("email"),
        "phones": [{"number": phone} for phone in customer.get("phones", [])]
    }


def prepare_order_data(order: Dict[str, Any]) -> Dict[str, Any]:
    """Подготовка данных заказа для RetailCRM"""
    return {
        "number": order.get("order_number", ""),
        "customer": {"id": order.get("customer_id", 0),
                     "nickName": order.get("first_name", "") + " " + order.get("last_name", "")},
        "items": order.get("items", [])
    }


def prepare_payment_data(
        order_id: int,
        amount: float,
        payment_type: str = "cash",
        comment: Optional[str] = None
) -> Dict[str, Any]:
    """Подготовка данных платежа для RetailCRM"""
    payment = {
        "order": {"id": order_id},
        "amount": amount,
        "type": payment_type
    }

    if comment:
        payment["comment"] = comment

    return payment
