import json

import httpx
from typing import Dict, Any, Optional
from app.config import settings


class RetailCRMService:
    def __init__(self):
        self.base_url = settings.retailcrm_api_url
        self.api_key = settings.retailcrm_api_key
        self.headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Универсальный метод для отправки запросов к RetailCRM API"""
        url = f"{self.base_url}/api/v5/{endpoint}"

        with httpx.Client() as client:
            response = client.request(
                method=method,
                url=url,
                headers=self.headers,
                **kwargs
            )
            response.raise_for_status()
            return response.json()

    # 1. Получение списка клиентов
    def get_customers(
            self,
            name: Optional[str] = None,
            email: Optional[str] = None,
            created_from: Optional[str] = None,
            created_to: Optional[str] = None,
            limit: int = 50,
            page: int = 1
    ) -> Dict[str, Any]:
        """Получение списка клиентов с фильтрацией"""
        params = {
            "limit": limit,
            "page": page
        }

        if name:
            params["filter[name]"] = name
        if email:
            params["filter[email]"] = email
        if created_from:
            params["filter[dateFrom]"] = created_from
        if created_to:
            params["filter[dateTo]"] = created_to

        return self._make_request("GET", "customers", params=params)

    # 2. Создание нового клиента
    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание нового клиента"""
        data = {
            "customer": json.dumps(customer_data, ensure_ascii=False)
        }
        return self._make_request("POST", "customers/create", data=data)

    # 3. Получение списка заказов клиента
    def get_customer_orders(
            self,
            customer_id: int,
            limit: int = 50,
            page: int = 1
    ) -> Dict[str, Any]:
        """Получение заказов клиента по его ID"""
        params = {
            "filter[customerId]": customer_id,
            "limit": limit,
            "page": page
        }

        return self._make_request("GET", "orders", params=params)

    # 4. Создание нового заказа
    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание нового заказа"""
        data = {
            "order": json.dumps(order_data, ensure_ascii=False)
        }
        return self._make_request("POST", "orders/create", data=data)

    # 5. Создание платежа
    def create_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Создание платежа для заказа"""
        data = {
            "payment": json.dumps(payment_data, ensure_ascii=False)
        }
        return self._make_request("POST", "orders/payments/create", data=data)


retailcrm_service = RetailCRMService()
