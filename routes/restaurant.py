from unittest import skip
from fastapi import APIRouter, Depends, HTTPException, Request, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from config.db import SessionLocal
import models, schemas
from crud import restaurant_crud, seller_crud
from routes.login import manager

router = APIRouter(
    prefix="/restaurant",
    tags=['Restaurants']
)

templates = Jinja2Templates(directory="public")

def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()

@router.get("/", response_class=HTMLResponse)
def read_restaurant_info(request: Request, user=Depends(manager)):
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    username = user.account_username

    print(f"ACCOUNT ID: {account_id}")
    seller_info = seller_crud.get_seller_by_account_id(db=db, account_id=account_id)
    seller_id = seller_info.seller_id
    print(f"SELLER ID: {seller_id}")
    restaurant_info = restaurant_crud.get_restaurant_info_by_seller_ID(db=db, seller_id=seller_id)
    print("Restaurant info: ",restaurant_info)

        
    data = []
    data.append(restaurant_info.__dict__)
    print(f"Restaurant info: {data}")

    data_res = {
        "request": request,
        "title": 'Xem món ăn',
        'restaurant_info': data,
        'username': username,
        'account_id': account_id
    }
    return templates.TemplateResponse("seller_restaurant_index.html", data_res)

@router.put("/edit-info")
async def update_restaurant_info(restaurant_id: int, restaurant: schemas.UpdateRestaurantInfo, request: Request, user= Depends(manager)):
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    print(f"Restaurant info: {restaurant.restaurant_name} - {restaurant.restaurant_address}")
    print(f"Restaurant ID: {restaurant_id}")

    restaurant_info = restaurant_crud.update_restaurant_info(db=db, restaurant=restaurant, restaurant_id=restaurant_id)
    status = 1
    message = ""
    if restaurant_info:
        status = 1
        message = "Cập nhật thành công"
    else:
        status = 0
        message = "Lỗi! Thử lại sau"

    return {"status": status, "message": message}

@router.put("/update-image")
async def update_restaurant_image(restaurant_id: int, request: Request, restaurant_image: UploadFile = File(...), user= Depends(manager) ):
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)
    print(f"Restaurant ID: {restaurant_id} ")
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

    restaurant_info = restaurant_crud.update_restaurant_image_by_restaurant_id(db=db, restaurant=restaurant, restaurant_id=restaurant_id)

    status = 1
    message = ""
    if restaurant_info:
        status = 1
        message = "Cập nhật thành công"
    else:
        status = 0
        message = "Lỗi! Thử lại sau"

    return {"status": status, "message": message}


@router.get("/{id}")
def get_restaurant(id: int):
    return restaurant_crud.get_restaurant_info_by_seller_ID(db=db, seller_id=id)

