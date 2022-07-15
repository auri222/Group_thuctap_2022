from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import SessionLocal
import models, schemas
from crud import account_crud
from ultilities import Hash
router = APIRouter(
    prefix="/account",
    tags=['Accounts']
)
def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()

@router.post("/create/")
def create_account(account: schemas.Account):
    plain = account.account_password
    account.account_password = Hash.bcrypt(password=plain)
    return account_crud.create_account(db, account=account)

@router.put("/update/{account_id}")
def update_account(account_id: int, account: schemas.Account):
    return account_crud.update_account(db=db, account=account, account_id=account_id)

@router.put("/update-password/{account_id}")
def update_account_password(account_id: int, account: schemas.UpdateAccountPassword):
    acc_id = account_crud.update_account_password(db=db, account=account, account_id=account_id)
    db_acc = db.query(models.Account).filter(models.Account.account_id == account_id).first()
    return db_acc

@router.put("/update-otp-token/{account_id}")
def update_account_password(account_id: int, account: schemas.UpdateAccountOTPToken):
    return account_crud.update_account_otp_token(db=db, account=account, account_id=account_id)

@router.delete("/delete/{account_id}")
def delete_account(account_id: int):
    return account_crud.delete_account(db, account_id=account_id)

@router.get("/check-duplicate-username")
def count_duplicate_username(username: str):
    db_ = get_database_session()
    count = account_crud.count_duplicate_username(db=db_, username=username)
    return {"count": count}

@router.get("/{id}")
def get_account(id: int):
    account = account_crud.get_account(db, account_id=id)
    return account

