"""
Typed row models for the database.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Customer:
    customer_id: str
    full_name: str
    email: str
    phone: Optional[str]
    city: Optional[str]
    created_at: str


@dataclass
class Product:
    product_id: str
    product_name: str
    category: Optional[str]
    brand: Optional[str]
    unit_price_inr: int
    returnable: bool


@dataclass
class Order:
    order_id: str
    customer_id: str
    product_id: str
    quantity: int
    order_date: str
    delivery_date: Optional[str]
    order_status: str
    payment_status: str
    payment_method: Optional[str]
    total_amount_inr: int


@dataclass
class ReturnRequest:
    return_id: str
    order_id: str
    customer_id: str
    request_date: str
    reason: Optional[str]
    return_status: str
    refund_status: str
    refund_amount_inr: Optional[int]