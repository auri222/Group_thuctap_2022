from sqlalchemy.orm import Session
import models
import schemas

def get_buyer_by_account_id(db: Session, account_id: int):
    return db.query(models.Buyer).filter(models.Buyer.account_id == account_id).first()

def get_buyer(db: Session, buyer_id: int):
    return db.query(models.Buyer).filter(models.Buyer.buyer_id == buyer_id).first()

def get_buyer_by_email(db: Session, email: str):
    return db.query(models.Buyer).filter(models.Buyer.buyer_email == email).first()

def get_buyers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Buyer).offset(skip).limit(limit).all()

def create_buyer(db: Session, buyer: schemas.CreateBuyerInfo):
    db_buyer = models.Buyer( buyer_name=buyer.buyer_name, 
                            buyer_birthday=buyer.buyer_birthday, 
                            buyer_address=buyer.buyer_address, 
                            buyer_phone=buyer.buyer_phone, 
                            buyer_email= buyer.buyer_email, 
                            buyer_shipping_address=buyer.buyer_shipping_address,
                            account_id = buyer.account_id)
    db.add(db_buyer)
    db.commit()
    db.refresh(db_buyer)
    return db_buyer

def create_buyer_return_ID(db: Session, buyer: schemas.CreateBuyerInfo, account_id: int):
    db_buyer = models.Buyer( buyer_name=buyer.buyer_name, 
                            buyer_birthday=buyer.buyer_birthday, 
                            buyer_address=buyer.buyer_address, 
                            buyer_phone=buyer.buyer_phone, 
                            buyer_email= buyer.buyer_email, 
                            buyer_shipping_address=buyer.buyer_shipping_address,
                            account_id = account_id)
    db.add(db_buyer)
    db.commit()
    buyer_id = db_buyer.buyer_id
    db.refresh(db_buyer)
    return buyer_id

def delete_buyer(db:Session,buyer_id:int):
    delete_buyer=db.query(models.Buyer).filter(models.Buyer.buyer_id == buyer_id).first()
    db.delete(delete_buyer)
    db.commit()
    return {"Success": f"Buyer with ID {buyer_id} is deleted"}

def update_buyer(db:Session,buyer: schemas.UpdateBuyerInfo, buyer_id: int):
    db_buyer=db.query(models.Buyer).filter(models.Buyer.buyer_id == buyer_id).first()

    db_buyer.buyer_name = buyer.buyer_name
    db_buyer.buyer_birthday = buyer.buyer_birthday
    db_buyer.buyer_address = buyer.buyer_address
    db_buyer.buyer_phone = buyer.buyer_phone
    db_buyer.buyer_email = buyer.buyer_email
    db_buyer.buyer_shipping_address = buyer.buyer_shipping_address

    db.commit()
    buyer_id = db_buyer.buyer_id
    return buyer_id

def update_buyer_return_buyer_id(db:Session, buyer: schemas.UpdateBuyerInfo, account_id: int):
    db_buyer=db.query(models.Buyer).filter(models.Buyer.account_id == account_id).first()

    db_buyer.buyer_name = buyer.buyer_name
    db_buyer.buyer_birthday = buyer.buyer_birthday
    db_buyer.buyer_address = buyer.buyer_address
    db_buyer.buyer_phone = buyer.buyer_phone
    db_buyer.buyer_email = buyer.buyer_email
    db_buyer.buyer_shipping_address = buyer.buyer_shipping_address

    db.commit()
    buyer_id = db_buyer.buyer_id
    return buyer_id

# Phân trang admin ----------------------------------------------------------
def count_all_rows_buyer(db: Session):
    query = f"""SELECT COUNT(*) AS TOTAL_ROW
FROM account acc
JOIN buyer b ON b.account_id = acc.account_id"""
    result = db.execute(query)
    return result.fetchall()

def get_all_buyers(db: Session, skip: int=0, limit: int=100):
    string = f"""SELECT acc.account_id, acc.account_username, b.*
                    FROM account acc
                    JOIN buyer b ON b.account_id = acc.account_id
                    """

    pagination = f"""LIMIT {skip}, {limit} """
    string = ''.join([string, pagination])
    result = db.execute(string)
    return result.fetchall()

def get_all_info_buyer(db: Session, buyer_id:int):
    string = f"""SELECT acc.account_username, acc.account_date_created, b.*
FROM buyer b
JOIN account acc ON acc.account_id = b.account_id
WHERE b.buyer_id = {buyer_id}"""
    result = db.execute(string)
    return result.fetchall()