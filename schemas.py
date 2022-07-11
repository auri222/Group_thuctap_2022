from typing import Union
from pydantic import BaseModel
from datetime import date, datetime

#Start Login
#----------------------------------------------------------
class Login(BaseModel):
    username: str
    password: str
    class Config:
        orm_mode = True

#End Login
#----------------------------------------------------------

#Start Account
#----------------------------------------------------------
class Account(BaseModel):
    account_username: str
    account_password: str
    account_type: int
    account_otp: Union[int, None] = None
    account_token: Union[str, None] = None
    account_verify_status: Union[int, None] = None
    account_active_status: Union[int, None] = None
    account_date_created: datetime = None

    class Config:
        orm_mode = True

class RegisterAccount(Account):
    pass

class AccountToken(BaseModel):
    account_id: int
    account_token: str

    class Config:
        orm_mode = True

class UpdateAccountName(BaseModel):
    account_username: str

    class Config:
        orm_mode = True

class UpdateAccountPassword(BaseModel):
    account_password: str

    class Config:
        orm_mode = True

class UpdateAccountVerifyStatus(BaseModel):
    account_verify_status: int

    class Config:
        orm_mode = True

class UpdateAccountActiveStatus(BaseModel):
    account_active_status: int

    class Config:
        orm_mode = True

class UpdateAccountOTPToken(BaseModel):
    account_otp: int
    account_token: str
    
    class Config:
        orm_mode = True

#End Account
#----------------------------------------------------------

#Start Admin
#----------------------------------------------------------
class Admin(BaseModel):
    admin_name: str
    admin_birthday: date = None
    admin_address: str
    admin_phone: str
    admin_email: str
    account_id : int

    class Config:
        orm_mode = True

class CreateAdminInfo(BaseModel):
    admin_name: str
    admin_birthday: date = None
    admin_address: str
    admin_phone: str
    admin_email: str

    class Config:
        orm_mode = True
class UpdateAdminInfo(BaseModel):
    admin_name: str
    admin_birthday: date = None
    admin_address: Union[str, None] = None
    admin_phone: str
    admin_email: str

    class Config:
        orm_mode = True
#End Admin
#----------------------------------------------------------

#Start Buyer
#----------------------------------------------------------
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

class CreateBuyerInfo(Buyer):
    pass

class UpdateBuyerInfo(BaseModel):
    buyer_name: str
    buyer_birthday: date = None
    buyer_address: Union[str, None] = None
    buyer_phone: str
    buyer_email: str
    buyer_shipping_address: str

    class Config:
        orm_mode = True

#End Buyer
#----------------------------------------------------------

#Start Seller
#----------------------------------------------------------
class Seller(BaseModel):
    seller_name: str
    seller_birthday: date = None
    seller_address: Union[str, None] = None
    seller_phone: str
    seller_email: str
    account_id: int

    class Config:
        orm_mode = True

class CreateSellerInfo(Seller):
    pass

class UpdateSellerInfo(BaseModel):
    seller_name: str
    seller_birthday: date = None
    seller_address: Union[str, None] = None
    seller_phone: str
    seller_email: str

    class Config:
        orm_mode = True

#End Seller
#----------------------------------------------------------

#Start Food type
#----------------------------------------------------------
class FoodType(BaseModel):
    food_type_name: str

    class Config:
        orm_mode = True

#End Food type
#----------------------------------------------------------

#Start Payment methods
#----------------------------------------------------------
class PaymentMethod(BaseModel):
    payment_method_name: str

    class Config:
        orm_mode = True

#End Payment methods
#----------------------------------------------------------

#Start Restaurant
#----------------------------------------------------------
class Restaurant(BaseModel):
    restaurant_name: str
    restaurant_address: str
    restaurant_image: Union[str, None] = None
    seller_id: int

    class Config:
        orm_mode = True

class CreateRestaurantInfo(BaseModel):
    restaurant_name: str
    restaurant_address: str
    restaurant_image: Union[str, None] = None
    class Config:
        orm_mode = True

class UpdateRestaurantInfo(BaseModel):
    restaurant_name: str
    restaurant_address: str

    class Config:
        orm_mode = True

class UpdateRestaurantImage(BaseModel):
    restaurant_image: str

    class Config:
        orm_mode = True


#End Restaurant
#----------------------------------------------------------

#Start Food
#----------------------------------------------------------
class Food(BaseModel):
    food_name: str
    food_image: Union[str, None] = None
    food_price: float
    food_description: Union[str, None] = None
    food_type_id: int

    class Config:
        orm_mode = True

class CreateFoodInfo(Food):
    pass

class UpdateFoodInfo(BaseModel):
    food_name: str
    food_price: float
    food_description: Union[str, None] = None
    food_type_id: int

    class Config:
        orm_mode = True

class UpdateFoodImage(BaseModel):
    food_image: str

    class Config:
        orm_mode = True

#End Food
#----------------------------------------------------------


#Start Restaurant warehouse
#----------------------------------------------------------
class RestaurantWarehouse(BaseModel):
    restaurant_id: int
    food_id: int
    food_quantity: int

    class Config:
        orm_mode = True

class CreateRestaurantWarehouse(BaseModel):
    food_quantity: int

    class Config:
        orm_mode = True

class UpdateRestaurantWarehouse(BaseModel):
    food_quantity: int

    class Config:
        orm_mode = True

#End Restaurant warehouse
#----------------------------------------------------------

#Start Order
#----------------------------------------------------------
class Order(BaseModel):
    order_created_date: datetime = None
    order_shipping_address: str
    order_status: int
    seller_id: int
    buyer_id: int
    payment_method_id: int

    class Config:
        orm_mode = True

#End Order
#----------------------------------------------------------

#Start Order Detail 
#----------------------------------------------------------
class OrderDetail(BaseModel):
    order_id: int
    food_id: int
    order_quantity: int
    order_price: float

    class Config:
        orm_mode = True

#End Order Detail
#----------------------------------------------------------