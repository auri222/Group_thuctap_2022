from operator import mod
import string
from typing import Union
from unittest import result
from sqlalchemy.orm import Session
import models
import schemas

def get_seller_by_id(db: Session, Seller_ID: int):
    return db.query(models.Seller).filter(models.Seller.seller_id == Seller_ID).first() 

def get_seller_by_account_id(db: Session, account_id: int):
    return db.query(models.Seller).filter(models.Seller.account_id == account_id).first() 

def get_seller_by_email(db: Session, email: str):
    return db.query(models.Seller).filter(models.Seller.seller_email == email).first()

def get_sellers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Seller).offset(skip).limit(limit).all()

def create_seller(db: Session, seller: schemas.CreateSellerInfo, account_id: int):
    db_seller = models.Seller(  seller_name=seller.seller_name,
                                seller_birthday= seller.seller_birthday,
                                seller_address = seller.seller_address, 
                                seller_phone = seller.seller_phone, 
                                seller_email = seller.seller_email,
                                account_id = account_id
    )
    db.add(db_seller)
    db.commit()
    seller_id = db_seller.seller_id
    db.refresh(db_seller)
    return db_seller

def create_seller_return_ID(db: Session, seller: schemas.CreateSellerInfo):
    db_seller = models.Seller(  seller_name=seller.seller_name,
                                seller_birthday= seller.seller_birthday,
                                seller_address = seller.seller_address, 
                                seller_phone = seller.seller_phone, 
                                seller_email = seller.seller_email,
                                account_id = seller.account_id
    )
    db.add(db_seller)
    db.commit()
    seller_id = db_seller.seller_id
    db.refresh(db_seller)
    return seller_id

# def delete_seller(db: Session, Seller_ID: int):
#     db_seller = db.query(models.Seller),filter(models.Seller.seller_id == Seller_ID).first()
#     if db_seller is None:
#         return {"Error": f"Seller with ID {Seller_ID} is not exits"}
#     db.delete(db_seller)
#     db.commit()
#     return {"Success": f"Seller with ID {Seller_ID} is deleted"}

def update_seller_return_ID(db: Session, seller: schemas.Seller, Seller_ID: int):
    update_sel = db.query(models.Seller).filter(models.Seller.seller_id == Seller_ID).first()
    if update_sel is None:
        return {"Error"}
    update_sel.seller_name = seller.seller_name
    update_sel.seller_birthday = seller.seller_birthday
    update_sel.seller_address = seller.seller_address
    update_sel.seller_phone = seller.seller_phone
    update_sel.seller_email = seller.seller_email
    db.commit()
    seller_id = update_sel.seller_id
    return seller_id
    
def update_seller_by_account_id(db: Session, seller: schemas.UpdateSellerInfo, account_id: int):
    update_sel = db.query(models.Seller).filter(models.Seller.account_id == account_id).first()

    update_sel.seller_name = seller.seller_name
    update_sel.seller_birthday = seller.seller_birthday
    update_sel.seller_address = seller.seller_address
    update_sel.seller_phone = seller.seller_phone
    update_sel.seller_email = seller.seller_email
    db.commit()
    seller_id = update_sel.seller_id
    return seller_id

# Phân trang admin ----------------------------------------------------------
def count_all_rows_seller(db: Session):
    query = f"""SELECT COUNT(*) AS TOTAL_ROW
FROM account acc
JOIN seller sl ON sl.account_id = acc.account_id
JOIN restaurant res ON res.seller_id = sl.seller_id"""
    result = db.execute(query)
    return result.fetchall()

def get_all_sellers(db: Session, skip: int=0, limit: int=100):
    string = f"""SELECT acc.account_id, acc.account_username, acc.account_active_status ,sl.*, 
res.restaurant_name, res.restaurant_address, res.restaurant_image
FROM account acc
JOIN seller sl ON sl.account_id = acc.account_id
JOIN restaurant res ON res.seller_id = sl.seller_id 
"""

    # Nếu có seach => str = Pho
    pagination = f"""LIMIT {skip}, {limit} """
    string = ''.join([string, pagination])
    result = db.execute(string)
    return result.fetchall()

def get_all_info_seller(db: Session, seller_id: int):
    string = f"""SELECT acc.account_username, acc.account_date_created, sl.*, res.restaurant_name, res.restaurant_address, res.restaurant_image, COUNT(rw.food_id) AS TOTAL_FOOD
FROM seller sl
JOIN account acc ON acc.account_id = sl.account_id
JOIN restaurant res ON res.seller_id = sl.seller_id
JOIN restaurant_warehouse rw ON rw.restaurant_id = res.restaurant_id
WHERE sl.seller_id = {seller_id}"""

    result = db.execute(string)
    return result.fetchall()

# Xóa tài khoản seller ----------------------------------------------------------------------
def count_restaurant_info(db: Session, seller_id: int): # kết quả trả ra có thể là (0, NULL)
    string = f"""SELECT COUNT(*) AS TOTAL_RESTAURANT_ROW, res.restaurant_id
FROM restaurant res
JOIN seller sl ON sl.seller_id = res.seller_id
WHERE sl.seller_id = {seller_id}"""

    result = db.execute(string)
    return result.fetchall()

def count_warehouse_info(db: Session, seller_id: int):
    string = f"""SELECT COUNT(*) AS TOTAL_WAREHOUSE_ROW
/*SELECT rw.food_id*/
FROM restaurant_warehouse rw
JOIN restaurant res ON res.restaurant_id = rw.restaurant_id
JOIN seller sl ON sl.seller_id = res.seller_id
WHERE sl.seller_id = {seller_id}"""

    result = db.execute(string)
    return result.fetchall()

# Nếu TOTAL_WAREHOUSE_ROW > 0
def get_list_foods(db: Session, seller_id: int):
    string = f"""SELECT rw.food_id
FROM restaurant_warehouse rw
JOIN restaurant res ON res.restaurant_id = rw.restaurant_id
JOIN seller sl ON sl.seller_id = res.seller_id
WHERE sl.seller_id = {seller_id}"""

    result = db.execute(string)
    return result.fetchall()

def get_acccount_id(db: Session, seller_id):
    string = f"""SELECT sl.account_id
FROM seller sl
WHERE sl.seller_id = {seller_id}"""

    result = db.execute(string)
    return result.fetchall()

def delete_warehouse_food_by_restaurant_id(db: Session, restaurant_id: int):
    # num_row_deleted = db.query(models.RestaurantWarehouse).filter(models.RestaurantWarehouse.restaurant_id == restaurant_id).delete()
    # db.commit()
    # return num_row_deleted
    string = f"""DELETE rw, f
FROM restaurant_warehouse rw
JOIN food f ON f.food_id = rw.food_id
WHERE rw.restaurant_id = {restaurant_id}"""
    db.execute(string) #-> Thực thi lệnh trong string
    db.commit() #-> commit để cập nhật những thay đổi đối với database (xóa)
    return {"success": True}

def delete_restaurant(db: Session, restaurant_id: int):
    num_row_deleted = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == restaurant_id).delete()
    db.commit()
    return num_row_deleted

def delete_seller(db: Session, seller_id: int):
    num_row_deleted = db.query(models.Seller).filter(models.Seller.seller_id == seller_id).delete()
    db.commit()
    return num_row_deleted

def delete_account(db: Session, account_id: int):
    num_row_deleted = db.query(models.Account).filter(models.Account.account_id == account_id).delete()
    db.commit()
    return num_row_deleted

