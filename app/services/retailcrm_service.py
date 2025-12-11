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
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """A universal method for sending requests to the RetailCRM API"""
        url = f"{self.base_url}/api/v5/{endpoint}"

        with httpx.Client() as client:
            response = client.request(
                method=method, url=url, headers=self.headers, **kwargs
            )
            response.raise_for_status()
            return response.json()

    def get_customers(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        created_from: Optional[str] = None,
        created_to: Optional[str] = None,
        limit: int = 50,
        page: int = 1,
    ) -> Dict[str, Any]:
        """Get list of customers with filters"""
        params = {"limit": limit, "page": page}

        if name:
            params["filter[name]"] = name
        if email:
            params["filter[email]"] = email
        if created_from:
            params["filter[dateFrom]"] = created_from
        if created_to:
            params["filter[dateTo]"] = created_to

        return self._make_request("GET", "customers", params=params)

    def create_customer(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new customer"""
        data = {"customer": json.dumps(customer_data, ensure_ascii=False)}
        return self._make_request("POST", "customers/create", data=data)

    def get_customer_orders(
        self, customer_id: int, limit: int = 50, page: int = 1
    ) -> Dict[str, Any]:
        """Get list of orders by customer ID"""
        params = {"filter[customerId]": customer_id, "limit": limit, "page": page}

        return self._make_request("GET", "orders", params=params)

    def create_order(self, order_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new order"""
        data = {"order": json.dumps(order_data, ensure_ascii=False)}
        return self._make_request("POST", "orders/create", data=data)

    def create_payment(self, payment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new payment for order"""
        data = {"payment": json.dumps(payment_data, ensure_ascii=False)}
        return self._make_request("POST", "orders/payments/create", data=data)


retailcrm_service = RetailCRMService()
