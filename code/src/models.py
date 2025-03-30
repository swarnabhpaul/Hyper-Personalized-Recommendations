from pydantic import BaseModel
from enum import Enum
from typing import List

class Product(BaseModel):
    pid: int
    bid: int
    product_name: str
    business_name: str
    popularity: float
    price: float
    geo_demand: str
    category: str

class LoginData(BaseModel):
    username: str
    password: str

class UserType(str, Enum):
    CUSTOMER = "customer"
    BUSINESS = "business"

# Model for category spend
class CategorySpend(BaseModel):
    category: str
    spend: float

# Model for payment mode spend
class PaymentModeSpend(BaseModel):
    mode: str
    spend: float

# Main model with list of categories and payment modes
class CustomerChart(BaseModel):
    category: List[CategorySpend]
    payment_mode: List[PaymentModeSpend]

# Model for business insight data
class BusinessInsight(BaseModel):
    action_items: List[str]
    questions: List[str]

class ProductRevenue(BaseModel):
    product_name: str
    amount: float

class PaymentModeRevenue(BaseModel):
    mode: str
    amount: float

class BusinessChart(BaseModel):
    products: List[ProductRevenue]
    payment_mode: List[PaymentModeRevenue]
