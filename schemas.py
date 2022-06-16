from typing import Union
from pydantic import BaseModel
from datetime import date, datetime

class Account(BaseModel):
    account_username: str
    account_password: str
    account_type: int
    account_otp: Union[int, None] = None
    account_token: Union[str, None] = None
    account_date_created: datetime = None

    class Config:
        orm_mode = True

class Admin(BaseModel):
    admin_name: str
    admin_birthday: date = None
    admin_addrs: str
    admin_phone: str
    admin_email: str
    account_id : int

    class Config:
        orm_mode = True

class Buyer(BaseModel):
    buyer_name: str
    buyer_birthday: date = None
    buyer_address: Union[str, None] = None
    buyer_phone: str
    buyer_email: str
    buyer_shipping_address: str
    account_id: int

    class Config:
        orm_mode = True

class Seller(BaseModel):
    seller_name: str
    seller_birthday: date = None
    seller_address: Union[str, None] = None
    seller_phone: str
    seller_email: str
    account_id: int

    class Config:
        orm_mode = True

class FoodType(BaseModel):
    food_type_name: str

    class Config:
        orm_mode = True

class PaymentMethod(BaseModel):
    payment_method_name: str

    class Config:
        orm_mode = True

class Restaurant(BaseModel):
    restaurant_name: str
    restaurant_address: str
    seller_id: int

    class Config:
        orm_mode = True

class Food(BaseModel):
    food_name: str
    food_image: Union[str, None] = None
    food_price: float
    food_description: Union[str, None] = None
    food_type_id: int

    class Config:
        orm_mode = True

class RestaurantWarehouse(BaseModel):
    restaurant_id: int
    food_id: int
    food_quantity: int

    class Config:
        orm_mode = True

class Order(BaseModel):
    order_created_date: datetime = None
    order_shipping_address: str
    order_status: int
    seller_id: int
    buyer_id: int
    payment_method_id: int

    class Config:
        orm_mode = True

class OrderDetail(BaseModel):
    order_id: int
    food_id: int
    order_quantity: int
    order_price: float

    class Config:
        orm_mode = True