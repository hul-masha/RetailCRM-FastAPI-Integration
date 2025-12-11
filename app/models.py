from enum import StrEnum
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class CustomerCreate(BaseModel):
    firstName: str = Field(min_length=1, description="Customer name")
    lastName: Optional[str] = Field(description="Customer surname")
    email: EmailStr
    phones: List[str] = Field(default_factory=list, description="List of phones")


class Response(BaseModel):
    success: bool
    id: int


class OrderItem(BaseModel):
    productName: str = Field(description="Product name")
    quantity: int = Field(1, ge=1, description="Amount")
    initialPrice: float = Field(0.1, gt=0, description="Price")


class OrderCreate(BaseModel):
    customer_id: int = Field(description="ID of existed customer")
    first_name: str = Field(min_length=1, description="Customer name")
    last_name: Optional[str] = Field(description="Customer surname")
    items: List[OrderItem] = Field(default_factory=list, description="List of products")
    order_number: str = Field(description="Order number")


class PaymentTypeEnum(StrEnum):
    cash = "cash"
    card = "card"


class PaymentCreate(BaseModel):
    order_id: int = Field(description="Order ID")
    amount: float = Field(0.1, gt=0, description="Payment amount")
    payment_type: PaymentTypeEnum = PaymentTypeEnum.cash
    comment: Optional[str] = None


class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
