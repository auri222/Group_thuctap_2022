from sqlalchemy.orm import Session
import models
import schemas
from ultilities import Hash
import os
def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.account_id == account_id).first()

def get_account_by_name(db: Session, account_name: str):
    return db.query(models.Account).filter(models.Account.account_username == account_name).first()

def create_account(db: Session, account: schemas.Account):
    hashed_password = Hash.bcrypt(account.account_password)
    db_acc = models.Account(
                        account_username = account.account_username,
                        account_password = hashed_password,
                        account_type = account.account_type,
                        account_otp = account.account_otp,
                        account_token = account.account_token,
                        account_verify_status = account.account_verify_status,
                        account_active_status = account.account_active_status,
                        account_date_created = account.account_date_created)
    db.add(db_acc)
    db.commit()
    db.refresh(db_acc)
    return db_acc

def create_account_return_ID(db: Session, account: schemas.Account):
    hashed_password = Hash.bcrypt(account.account_password)
    db_acc = models.Account(
                        account_username = account.account_username,
                        account_password = hashed_password,
                        account_type = account.account_type,
                        account_otp = account.account_otp,
                        account_token = account.account_token,
                        account_verify_status = account.account_verify_status,
                        account_active_status = account.account_active_status,
                        account_date_created = account.account_date_created)
    db.add(db_acc)
    db.commit()
    acc_id = db_acc.account_id
    db.refresh(db_acc)
    return acc_id

def update_account(db: Session, account: schemas.Account, account_id: int):
    db_acc = db.query(models.Account).filter(models.Account.account_id == account_id).first()
    if db_acc is None:
        return {"Error": f"Account with ID {account_id} is not exists"}
    db_acc.account_username = account.account_username
    db_acc.account_password = account.account_password
    db_acc.account_type = account.account_type
    db_acc.account_otp = account.account_otp
    db_acc.account_token = account.account_token
    db_acc.account_verify_status = account.account_verify_status,
    db_acc.account_active_status = account.account_active_status,
    db_acc.account_date_created = account.account_date_created

    db.commit()
    return db_acc

def update_account_password(db: Session, account: schemas.UpdateAccountPassword, account_id: int):
    db_acc = db.query(models.Account).filter(models.Account.account_id == account_id).first()
    if db_acc is None:
        return {"Error": f"Account with ID {account_id} is not exists"}
    hashed_password = Hash.bcrypt(account.account_password)
    db_acc.account_password = hashed_password
    db.commit()
    acc_id = db_acc.account_id
    return acc_id

def update_account_otp_token(db: Session, account: schemas.UpdateAccountOTPToken, account_id: int):
    db_acc = db.query(models.Account).filter(models.Account.account_id == account_id).first()
    if db_acc is None:
        return {"Error": f"Account with ID {account_id} is not exists"}
    hashed_password = Hash.bcrypt(account.account_password)
    token = os.urandom(24).hex()
    db_acc.account_password = hashed_password
    db_acc.account_token = token
    db.commit()
    return db_acc

def delete_account(db: Session, account_id: int):
    db_acc = db.query(models.Account).filter(models.Account.account_id == account_id).first()
    if db_acc is None:
        return {"Error": f"Account with ID {account_id} is not exists"}
    db.delete(db_acc)
    db.commit()
    return {"Success": f"Account with ID {account_id} is deleted"}