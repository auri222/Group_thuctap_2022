from sqlalchemy.orm import Session
import models
import schemas

def get_all_payment_method(db: Session, skip: int = 0, limit: int = 100): 
    return db.query(models.PaymentMethod).offset(skip).limit(limit).all()

def create_payment_method(db: Session, payment_method: schemas.PaymentMethod):
    db_payment_method = models.PaymentMethod(payment_method_name = payment_method.payment_method_name)
    db.add(db_payment_method)
    db.commit()
    db.refresh(db_payment_method)
    return db_payment_method

def get_payment_method_by_ID(db: Session, payment_id: int):
    db_payment = db.query(models.PaymentMethod).filter(models.PaymentMethod.payment_method_id == payment_id).first()
    if db_payment is None:
        return {"Error": f"Food type of this ID {payment_id} is not exists"}
    return db_payment

def count_payment_method(db: Session, payment_method_name: str):
    return db.query(models.PaymentMethod).filter(models.PaymentMethod.payment_method_name == payment_method_name).count()

def update_payment_method(db: Session, payment_method: schemas.PaymentMethod, payment_id: int):
    db_payment = db.query(models.PaymentMethod).filter(models.PaymentMethod.payment_method_id == payment_id).first()
    if db_payment is None:
        return {"Error": f"Food type of this ID {payment_id} is not exists"}
    db_payment.payment_method_name = payment_method.payment_method_name
    db.commit()
    db_payment_id = db_payment.payment_method_id
    return db_payment_id

def delete_payment_method(db: Session, payment_id: int):
    db_payment = db.query(models.PaymentMethod).filter(models.PaymentMethod.payment_method_id == payment_id).first()
    if db_payment is None:
        return {"Error": f"Food type of this ID {payment_id} is not exists"}
    db.delete(db_payment)
    db.commit()
    return {"Success": "Delete payment method successfully"}