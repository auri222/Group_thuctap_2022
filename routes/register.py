from email import message
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
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

@router.get("/", response_class=HTMLResponse)
def register_account(request: Request):

    data_res = {
        "request": request,
        "title": "Trang đăng ký",
    }

    return templates.TemplateResponse("register_account.html", data_res)

@router.get("/count")
def count(username: str):
    dupplicate_row = account_crud.count_duplicate_username(db, username=username)
    return {"Count": dupplicate_row}

@router.post("/")
async def handle_register_account_form(register_account: schemas.RegisterAccount):
    otp = random.randint(0,999999)
    url_token = os.urandom(24).hex()
    register_account.account_otp = otp
    register_account.account_token = url_token
    register_account.account_verify_status = 1
    register_account.account_active_status = 0
    username = register_account.account_username
    print(username)
    dupplicate_row = account_crud.count_duplicate_username(db, username=username)

    if dupplicate_row > 0:
        status = 0
        message = "Tên đăng nhập bị trùng! Hãy nhập lại"
        account_id = 0
    else:
        account_id = account_crud.create_account_return_ID(db=db, account=register_account)
        if account_id != None:
            status = 1
            message = "Đăng ký tài khoản thành công!"
        else:
            status = 0
            message = "Hệ thống lỗi! Vui lòng thử lại sau!"
    
    return {"status": status, "message": message, "account_id": account_id}

@router.get("/register-seller/", response_class=HTMLResponse)
async def register_seller(request: Request, account_id: int):

    data_res = {
        "request": request,
        "title": "Trang đăng ký thông tin người bán",
        'account_id': account_id
    }

    return templates.TemplateResponse("register_seller_info.html", data_res)

@router.post("/register-seller/")
async def handle_register_seller_form(register_seller: schemas.CreateSellerInfo, register_restaurant: schemas.CreateRestaurantInfo):
    #Khởi tạo biến thông báo
    status = 1
    message = ""
    
    seller_id = seller_crud.create_seller_return_ID(db=db, seller=register_seller)
    if seller_id:
        data_restaurant = restaurant_crud.create_restaurant_info(db=db, restaurant=register_restaurant, seller_id=seller_id)
        if data_restaurant:
            status = 1
            message = "Đăng ký thông tin thành công"
        else:
            status = 0
            message = "Lỗi. Hãy thử lại sau!"
    else:
        status = 0
        message = "Lỗi. Hãy thử lại sau!"
        seller_id = 0
    print(register_seller)
    print(register_restaurant)
    print(data_restaurant.__dict__)
    return {"status": status, "message": message, "seller_id": seller_id}

@router.put("/register-seller/{seller_id}")
async def handle_restaurant_image(seller_id: int, restaurant_image: UploadFile = File(...)):
    
    print(seller_id)
    #Xử lý ảnh
    #-------------------------------------------
    filename = restaurant_image.filename
    content = await restaurant_image.read()
    PATH = "./static/backend/seller/images/restaurant_avatar/"
    FILEPATH = PATH + filename
    with open(FILEPATH, "wb") as f:
        f.write(content)
    #--------------------------------------------
    restaurant = schemas.UpdateRestaurantImage
    restaurant.restaurant_image = filename
    
    db_restaurant = restaurant_crud.update_restaurant_image(db=db, restaurant=restaurant, seller_id=seller_id)
    
    status = 1
    message = ""

    if db_restaurant:
        status = 1
        message = "Đăng ký thông tin thành công"
    else:
        status = 0
        message = "Lỗi lưu thông tin. Hãy thử lại sau!"
    print(db_restaurant.__dict__)
    return {"status": status, "message": message}

@router.get("/register-buyer", response_class=HTMLResponse)
def register_buyer(request: Request, account_id: int):

    data_res = {
        "request": request,
        "title": "Trang đăng ký thông tin người mua",
        'account_id': account_id
    }

    return templates.TemplateResponse("register_buyer_info.html", data_res)

@router.post("/register-buyer")
def handle_register_buyer_form(register_buyer: schemas.CreateBuyerInfo):
    #Khởi tạo biến thông báo
    status = 1
    message = ""

    buyer_info = buyer_crud.create_buyer(db=db, buyer=register_buyer)
    if buyer_info:
        status = 1
        message = "Đăng ký thông tin thành công!"
    else:
        status = 0 
        message = "Lỗi. Vui lòng thử lại sau!"
    print(buyer_info.__dict__)
    return {"status": status,"message": "Đăng ký thành công"}