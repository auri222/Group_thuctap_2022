from sqlalchemy.orm import Session
import models
import schemas
from ultilities import Hash
import os
def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.account_id == account_id).first()

def get_account_username(db: Session, account_id: int):
    db_acc = db.query(models.Account).filter(models.Account.account_id == account_id).first()
    username = db_acc.account_username
    return username

def get_account_by_name(db: Session, account_name: str):
    return db.query(models.Account).filter(models.Account.account_username == account_name).first()

def count_duplicate_username(db: Session, username: str):
    count = db.execute(f"""SELECT COUNT(*) as TOTAL FROM account WHERE account_username='{username}' """)
    return count.fetchall()

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

def update_account_name(db: Session, account: schemas.UpdateAccountName, account_id: int):
    db_acc = db.query(models.Account).filter(models.Account.account_id == account_id).first()
    db_acc.account_username = account.account_username
    db.commit()
    #Check dữ liệu trả ra có không
    username = db_acc.account_username
    return username

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
    password = db_acc.account_password
    return password

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

def update_account_active_status(db: Session, account_id: int, status: int = 1):
    db_acc = db.query(models.Account).filter(models.Account.account_id == account_id).first()

    db_acc.account_active_status = status
    db.commit()
    result = db_acc.account_active_status
    return result

def delete_account(db: Session, account_id: int):
    db_acc = db.query(models.Account).filter(models.Account.account_id == account_id).first()
    if db_acc is None:
        return {"Error": f"Account with ID {account_id} is not exists"}
    db.delete(db_acc)
    db.commit()
    return {"Success": f"Account with ID {account_id} is deleted"}

# Kiểm tra email từ các bảng admin, seller, buyer
# Nếu count> 0 thì lấy kết quả kiểm tra và return
def count_seller_by_email(db: Session, email: str):
    string = f"""SELECT COUNT(*) AS total_seller
                FROM seller sl
                WHERE sl.seller_email = '{email}'"""
    result = db.execute(string)
    return result.fetchall()

def count_buyer_by_email(db: Session, email: str):
    string = f"""SELECT COUNT(*) AS total_buyer
            FROM buyer b
            WHERE b.buyer_email = '{email}'"""
    result = db.execute(string)
    return result.fetchall()

def count_admin_by_email(db: Session, email: str):
    string = f"""SELECT COUNT(*) AS total_admin
            FROM admin ad
            WHERE ad.admin_email = '{email}'"""
    result = db.execute(string)
    return result.fetchall()

def get_account_by_email(db: Session, email: str, type: int):
    string = ""
    if type == 1:
        string = f"""SELECT acc.account_id, acc.account_token
                FROM admin ad
                JOIN account acc ON acc.account_id = ad.account_id
                WHERE ad.admin_email = '{email}'"""
    if type == 2:
        string = f"""SELECT acc.account_id, acc.account_token
                    FROM seller sl
                    JOIN account acc ON acc.account_id = sl.account_id
                    WHERE sl.seller_email = '{email}'"""
    if type == 3:
        string = f"""SELECT acc.account_id, acc.account_token
                    FROM buyer b
                    JOIN account acc ON acc.account_id = b.account_id
                    WHERE b.buyer_email = '{email}'"""
    result = db.execute(string)
    return result.fetchall()

def check_account_token(db: Session, token: str, id: int):
    string = f"""SELECT COUNT(*) AS TOTAL_ACCOUNT
FROM account acc
WHERE (acc.account_id = {id}) AND (acc.account_token = '{token}')"""
    result = db.execute(string)
    return result.fetchall()
