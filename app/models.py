from enum import StrEnum
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class CustomerCreate(BaseModel):
    firstName: str = Field(min_length=1, description="Имя клиента")
    lastName: Optional[str] = Field(description="Фамилия клиента")
    email: EmailStr
    phones: List[str] = Field(default_factory=list, description="Список телефонов")


class Response(BaseModel):
    success: bool
    id: int


class OrderItem(BaseModel):
    productName: str = Field(description="Название товара")
    quantity: int = Field(1, ge=1, description="Количество")
    initialPrice: float = Field(0.1, gt=0, description="Цена за единицу")


class OrderCreate(BaseModel):
    customer_id: int = Field(description="ID существующего клиента")
    first_name: str = Field(min_length=1, description="Имя клиента")
    last_name: Optional[str] = Field(description="Фамилия клиента")
    items: List[OrderItem] = Field(default_factory=list, description="Список продуктов")
    order_number: str = Field(description="Номер заказа")


class PaymentTypeEnum(StrEnum):
    cash = 'cash'
    card = 'card'

class PaymentCreate(BaseModel):
    order_id: int = Field(description="ID заказа")
    amount: float = Field(0.1, gt=0, description="Сумма платежа")
    payment_type: PaymentTypeEnum = PaymentTypeEnum.cash
    comment: Optional[str] = None


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
