from sqlalchemy import ForeignKey, Integer
from sqlalchemy.schema import Column
from sqlalchemy.types import String, Date, Integer, DateTime, Text, Float
from sqlalchemy.orm import relationship
from config.db import Base

class Account(Base):
    __tablename__ = "account"
    account_id = Column(Integer, primary_key=True, index=True)
    account_username = Column(String(100))
    account_password = Column(String(255))
    account_type = Column(Integer)
    account_otp = Column(Integer)
    account_token = Column(String(255))
    account_verify_status = Column(Integer)
    account_active_status = Column(Integer)
    account_date_created = Column(DateTime)


class Admin(Base):
    __tablename__ = "admin"
    admin_id = Column(Integer, primary_key=True, index=True)
    admin_name = Column(String(100))
    admin_birthday = Column(Date)
    admin_address = Column(String(250))
    admin_phone = Column(String(10))
    admin_email = Column(String(250))
    account_id = Column(Integer)


class Buyer(Base):
    __tablename__= "buyer"
    buyer_id = Column(Integer, primary_key=True, index=True)
    buyer_name = Column(String(100))
    buyer_birthday = Column(Date)
    buyer_address = Column(String(250), nullable=True)
    buyer_phone = Column(String(10))
    buyer_email = Column(String(250))
    buyer_shipping_address = Column(String(250))
    account_id = Column(Integer)


class Seller(Base):
    __tablename__= "seller"
    seller_id = Column(Integer, primary_key=True, index=True)
    seller_name = Column(String(100))
    seller_birthday = Column(Date)
    seller_address = Column(String(250), nullable=True)
    seller_phone = Column(String(10))
    seller_email = Column(String(250))
    account_id = Column(Integer)

class FoodType(Base):
    __tablename__ = "food_type"
    food_type_id = Column(Integer, primary_key=True, index=True)
    food_type_name = Column(String(250))

class PaymentMethod(Base):
    __tablename__ = "payment_method"
    payment_method_id = Column(Integer, primary_key=True, index=True)
    payment_method_name = Column(String(100))

class Restaurant(Base):
    __tablename__ = "restaurant"
    restaurant_id = Column(Integer, primary_key=True, index=True)
    restaurant_name = Column(String(250))
    restaurant_address = Column(String(250))
    restaurant_image = Column(String(255), nullable=True)
    seller_id = Column(Integer)

class Food(Base):
    __tablename__ = "food"
    food_id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String(250))
    food_image = Column(String(250))
    food_price = Column(Float)
    food_description = Column(Text)
    food_type_id = Column(Integer)

class RestaurantWarehouse(Base):
    __tablename__ = "restaurant_warehouse"
    restaurant_id = Column(Integer, primary_key=True)
    food_id = Column(Integer, primary_key=True)
    food_quantity = Column(Integer)

class Order(Base):
    __tablename__ = "order"
    order_id = Column(Integer, primary_key=True, index=True)
    order_created_date = Column(DateTime)
    order_shipping_address = Column(String(250))
    order_status = Column(Integer)
    seller_id = Column(Integer)
    buyer_id = Column(Integer)
    payment_method_id = Column(Integer)

class OrderDetail(Base):
    __tablename__ = "order_detail"
    order_id = Column(Integer, primary_key=True)
    food_id = Column(Integer, primary_key=True)
    order_quantity = Column(Integer)
    order_price = Column(Float)