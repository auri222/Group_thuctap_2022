from sqlalchemy.orm import Session
import models
import schemas

def get_seller(db: Session, Seller_ID: int):
    return db.query(models.Seller).filter(models.Seller.seller_id == Seller_ID).first() 

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
    
