from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from config.db import SessionLocal
import models, schemas
from crud import account_crud, seller_crud, buyer_crud, restaurant_crud
from numpy import random
from ultilities import Hash
import os
router = APIRouter(
    prefix="/register",
    tags=['Register']
)
def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()

templates = Jinja2Templates(directory="public")

@router.get("/register", response_class=HTMLResponse)
def register_account(request: Request):

    data_res = {
        "request": request,
        "title": "Trang đăng ký",
    }

    return templates.TemplateResponse("", data_res)

@router.post("/register")
def handle_register_account_form(register_account: schemas.RegisterAccount):
    otp = random.randint(0,999999)
    url_token = os.urandom(24).hex()
    register_account.account_otp = otp
    register_account.account_token = url_token
    register_account.account_verify_status = 1
    register_account.account_active_status = 0

    account_id = account_crud.create_account_return_ID(db=db, account=register_account)

    return {"Success": "Đăng ký thành công", "account_id": account_id}

@router.get("/register/register-seller", response_class=HTMLResponse)
def register_seller(request: Request, account_id: int):

    data_res = {
        "request": request,
        "title": "Trang đăng ký thông tin người bán",
        'account_id': account_id
    }

    return templates.TemplateResponse("", data_res)

@router.post("/register/register-seller")
def handle_register_seller_form(register_seller: schemas.CreateSellerInfo, account_id: int, register_restaurant: schemas.CreateRestaurantInfo):
    seller_id = seller_crud.create_seller_return_ID(db=db, seller=register_seller, account_id=account_id)
    restaurant_info = restaurant_crud.create_restaurant_info(db=db, restaurant=register_restaurant, seller_id=seller_id)

    return {"Success": "Đăng ký thông tin thành công"}

@router.get("/register/register-buyer", response_class=HTMLResponse)
def register_buyer(request: Request, account_id: int):

    data_res = {
        "request": request,
        "title": "Trang đăng ký thông tin người mua",
        'account_id': account_id
    }

    return templates.TemplateResponse("", data_res)

@router.post("/register/register-buyer")
def handle_register_buyer_form(register_buyer: schemas.CreateBuyerInfo, account_id: int):
    buyer_id = buyer_crud.create_buyer_return_ID(db=db, buyer=register_buyer, account_id=account_id)

    return {"Success": "Đăng ký thành công", "ID": buyer_id}