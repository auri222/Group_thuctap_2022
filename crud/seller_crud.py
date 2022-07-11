import string
from typing import Union
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

def delete_seller(db: Session, Seller_ID: int):
    db_seller = db.query(models.Seller),filter(models.Seller.seller_id == Seller_ID).first()
    if db_seller is None:
        return {"Error": f"Seller with ID {Seller_ID} is not exits"}
    db.delete(db_seller)
    db.commit()
    return {"Success": f"Seller with ID {Seller_ID} is deleted"}

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
    string = f"""SELECT acc.account_id, acc.account_username, sl.*, 
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