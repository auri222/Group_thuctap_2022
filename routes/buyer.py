from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from requests import get
from sqlalchemy.orm import Session
from config.db import SessionLocal
from fastapi.templating import Jinja2Templates
import models, schemas
from crud import buyer_crud, account_crud, restaurant_crud
from routes.login import manager
router = APIRouter(
    prefix="/buyer",
    tags=['Buyers']
)
def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()

templates = Jinja2Templates(directory="public")

@router.get("/profile", response_class=HTMLResponse)
def buyer_profile(request: Request, user= Depends(manager)):
    if user.account_type != 3:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)
    account_id = user.account_id

    db_ = get_database_session()
    buyer_info = buyer_crud.get_buyer_by_account_id(db=db_, account_id=account_id)
    account_info = account_crud.get_account(db=db_, account_id=account_id)

    buyer_data = []
    buyer_data.append(buyer_info.__dict__)

    account_data = []
    account_data.append(account_info.__dict__)

    data_res = {
        "request": request,
        "title": "Trang thông tin người mua",
        'account_id': account_id,
        'buyer_info': buyer_data,
        'account_info': account_data
    }

    return templates.TemplateResponse("buyer_profile.html", data_res)

@router.get("/", response_class=HTMLResponse)
def home( request: Request, user= Depends(manager)):
    if user.account_type != 3:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)
    account_id = user.account_id
    db_ = get_database_session()
    account_info = account_crud.get_account(db=db_, account_id=account_id)
    username = account_info.account_username
    

    restaurant_info = restaurant_crud.get_all_restaurants(db=db_, skip=0, limit=10)

    restaurant_data = []
    for info in restaurant_info:
        restaurant_data.append(info)
    data_res = {
        "request": request,
        "title": "Trang chủ",
        'account_id': account_id,
        'username': username,
        'restaurant_info': restaurant_data
    }

    return templates.TemplateResponse("buyer_index.html",data_res)

