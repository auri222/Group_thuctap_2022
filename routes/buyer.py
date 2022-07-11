from email import message
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from requests import get
from sqlalchemy.orm import Session
from config.db import SessionLocal
from fastapi.templating import Jinja2Templates
import models, schemas
from crud import buyer_crud, account_crud, restaurant_crud, food_crud
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

    username = account_info.account_username

    buyer_data = []
    buyer_data.append(buyer_info.__dict__)

    account_data = []
    account_data.append(account_info.__dict__)

    data_res = {
        "request": request,
        "title": "Trang thông tin người mua",
        'account_id': account_id,
        'buyer_info': buyer_data,
        'account_info': account_data,
        'username': username
    }

    return templates.TemplateResponse("buyer_profile.html", data_res)

@router.put("/profile/edit-info")
async def edit_account(buyer: schemas.UpdateBuyerInfo, request: Request, user=Depends(manager)):
    if user.account_type != 3:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)
    account_id = user.account_id

    #Biến response kết quả
    status = 1
    message = ""

    buyer_info = buyer_crud.update_buyer_return_buyer_id(db=db, buyer=buyer, account_id=account_id)

    if buyer_info:
        status = 1
        message = "Cập nhật thông tin thành công"
    else: 
        status = 0
        message = "Cập nhật không thành công. Thử lại sau!"

    return {"status": status, "message": message}

@router.put("/profile/edit-account")
async def edit_account(account: schemas.UpdateAccountName, request: Request, user=Depends(manager)):
    if user.account_type != 3:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)
    account_id = user.account_id

    #Biến response kết quả
    status = 1
    message = ""

    #username lấy từ form
    username = account.account_username

    account_username = account_crud.update_account_name(db=db, account=account, account_id=account_id)

    if account_username:
        if account_username == username:
            status = 1
            message = "Cập nhật thông tin thành công"
        else:
            status = 0
            message = "Cập nhật thông tin không thành công"
    else: 
        status = 0
        message = "Cập nhật không thành công. Thử lại sau!"

    return {"status": status, "message": message}


@router.get("/restaurants", response_class=HTMLResponse)
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
    
    # Lấy dữ liệu để phân trang
    count = restaurant_crud.count_all_restaurants(db=db_)
    TOTAL_ROWS = count[0]['TOTAL_RESTAURANT']
    offset = 0
    limit = TOTAL_ROWS

    restaurant_info = restaurant_crud.get_all_restaurants(db=db_, skip=offset, limit=limit)

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

    return templates.TemplateResponse("restaurant_list.html",data_res)

@router.get("/restaurant-detail", response_class=HTMLResponse)
def home(restaurant_id: int, request: Request, user= Depends(manager)):
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
    
    # Lấy thông tin nhà hàng dựa trên ID
    restaurant_info = restaurant_crud.get_restaurant_info_by_ID(db=db_, restaurant_id=restaurant_id)

    restaurant_data = []
    restaurant_data.append(restaurant_info.__dict__)

    # Lấy danh sách món ăn dựa trên ID nhà hàng
    food_info = food_crud.get_food_from_restaurant(db=db_, restaurant_id=restaurant_id, skip=0, limit=100)
    food_data = []
    for food in food_info:
        food_data.append(food)
    
    # Lấy loại thức ăn của nhà hàng 
    food_type_info = restaurant_crud.get_list_food_type_by_restaurant_id(db=db_, restaurant_id=restaurant_id)
    food_type_data = []
    for food_type in food_type_info:
        food_type_data.append(food_type)

    data_res = {
        "request": request,
        "title": "Trang chủ",
        'account_id': account_id,
        'username': username,
        'restaurant_info': restaurant_data,
        'food_info': food_data,
        'food_type_info': food_type_data
    }

    return templates.TemplateResponse("restaurant_index.html",data_res)

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

