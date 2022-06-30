from fastapi import APIRouter, Depends, HTTPException, Request, File, Form, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from requests import session
from sqlalchemy.orm import Session
from config.db import SessionLocal
import models, schemas
from crud import restaurant_warehouse_crud, seller_crud, account_crud, food_crud, restaurant_crud
from routes.login import manager

router = APIRouter(
    prefix="/food",
    tags=['Foods']
)

templates = Jinja2Templates(directory="public")

def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()



# @router.get("/list_food/{account_id}", response_class=HTMLResponse)
# def read_list_food(account_id: int, request: Request, user=Depends(manager)):
#     if user.account_type != 2:
#         error_data = {
#             "request": request,
#             "title": 'Trang đăng nhập',
#             'error': 'Bạn không được cấp quyền để vào trang này!'
#         }
#         return templates.TemplateResponse("login.html", error_data)

    
#     seller_info = seller_crud.get_seller(db=db, account_id=account_id)
#     id = seller_info.seller_id
#     account_info = account_crud.get_account(db, account_id=account_id)
    
#     food_info = food_crud.get_food(db=db, seller_id = seller_info.seller_id)
#     username = account_info.account_username
#     data = []
#     for i in food_info:
#         data.append(i.__dict__)
#     data_res = {
#         "request": request,
#         "title": 'Danh sách món ăn',
#         'food_info': data,
#         'username': username,
#         'account_id': account_id
#     }
#     return templates.TemplateResponse("seller_list_food.html", data_res)

# @router.get("/show_food/{food_id}", response_class=HTMLResponse)
# def read_one_food(food_id: int, request: Request, user=Depends(manager)):
#     account_id = user.account_id
#     if user.account_type != 2:
#         error_data = {
#             "request": request,
#             "title": 'Trang đăng nhập',
#             'error': 'Bạn không được cấp quyền để vào trang này!'
#         }
#         return templates.TemplateResponse("login.html", error_data)

#     seller_info = seller_crud.get_seller(db=db, account_id=account_id)
#     account_info = account_crud.get_account(db, account_id=account_id)
#     food_info = food_crud.get_only_food(db=db, food_id=food_id)
#     data = []
#     data.append(food_info.__dict__)
#     data_res = {
#         "request": request,
#         "title": 'Xem món ăn',
#         'food_info': data,
#     }
#     return templates.TemplateResponse("seller_show_food.html", data_res)

@router.post("/create")
async def create_food_info(food: schemas.CreateFoodInfo, warehouse: schemas.CreateRestaurantWarehouse, request: Request, user=Depends(manager)):
    account_id = user.account_id
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    print(f"Food: {food}")
    print(f"Warehouse: {warehouse}")

    # Lấy ID Seller
    seller_info = seller_crud.get_seller_by_account_id(db=db, account_id=account_id)
    seller_id = seller_info.seller_id
    # Lấy ID restaurant 
    restaurant_info = restaurant_crud.get_restaurant_info_by_seller_ID(db=db, seller_id=seller_id)
    restaurant_id = restaurant_info.restaurant_id

    print(f"seller id: {seller_id} - restaurant id: {restaurant_id}")

    status = 1
    message = ""

    food_id = food_crud.create_food_info_return_ID(db=db, food=food)

    if food_id:
        restaurant_warehouse_info = restaurant_warehouse_crud.create_restaurant_warehouse_info(db=db, restaurant_warehouse=warehouse, restaurant_id=restaurant_id, food_id=food_id)
        if restaurant_info:
            status = 1
            message = "Thêm thông tin món ăn thành công"
        else:
            status = 0
            message = "Lỗi thêm số lượng món ăn. Thử lại sau."
    else:
        status = 0
        message = "Lỗi thêm thông tin món ăn. Thử lại sau."

    return {"status": status, "message": message, "food_id": food_id}

@router.put("/create/image")
async def read_one_food(food_id: int, request: Request, food_image: UploadFile = File(...), user=Depends(manager)):
    account_id = user.account_id
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    print(f"Food ID: {food_id}")

    #Xử lý ảnh
    #-------------------------------------------
    filename = food_image.filename
    content = await food_image.read()
    PATH = "./static/backend/seller/images/food/"
    FILEPATH = PATH + filename
    with open(FILEPATH, "wb") as f:
        f.write(content)

    food = schemas.UpdateFoodImage
    food.food_image = filename

    food_info = food_crud.update_food_image(db=db, food=food, food_id=food_id)

    print(f"Food info: {food_info}")

    status = 1
    message = ""

    if food_info:
        status = 1
        message = "Thêm thông tin thành công"
    else:
        status = 0
        message = "Lỗi thêm ảnh. Thử lại sau"

    return {"status": status, "message": message}

@router.get("/all")
def get_all_foods(acc_id: int):
    session = get_database_session()
    return food_crud.get_food_from_account(db=session, account_id=acc_id, skip=0, limit=100)
