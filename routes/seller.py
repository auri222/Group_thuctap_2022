from email import message
from typing import Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Request, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from regex import D
from sqlalchemy.orm import Session
from config.db import SessionLocal
import models, schemas
from crud import seller_crud, account_crud, food_type_crud, food_crud, order_crud
from routes.login import manager
import math
router = APIRouter(
    prefix="/seller",
    tags=['Sellers']
)

templates = Jinja2Templates(directory="public")

def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()


# @router.get("/all")
# def read_sellers(skip: int = 0, limit: int=100):
#     sellers = seller_crud.get_sellers(db, skip=skip, limit=limit)
#     return sellers

# @router.post("/create/{account_id}")
# def create_seller(account_id: int, seller: schemas.CreateSellerInfo, db: Session = Depends(get_database_session)):
#     return seller_crud.create_seller(db, seller=seller, account_id=account_id)

# @router.delete("/delete/{id}")
# def seller_detele(id: int, db: Session = Depends(get_database_session)):
    
#     return seller_crud.delete_seller(db,id)

# @router.put("/update/")
# def seller_update(seller: schemas.Seller, db: Session = Depends(get_database_session)):
#     update_sel = seller_crud.update_seller(db,seller=seller)
#     return seller_crud.get_seller(db, update_sel)



@router.get("/profile", response_class=HTMLResponse)
def read_profile_seller(request: Request, user=Depends(manager)):
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    created_date = user.account_date_created

    db_ = get_database_session()
    seller_info = seller_crud.get_seller_by_account_id(db=db_, account_id=account_id)

    username = account_crud.get_account_username(db=db_, account_id=account_id)

    data = []
    data.append(seller_info.__dict__)
    data_res = {
        "request": request,
        "title": 'Thông tin Seller',
        'seller_info': data,
        'username': username,
        'account_id': account_id,
        'created_date': created_date
    }
    return templates.TemplateResponse("seller_profile.html", data_res)

@router.put("/profile/edit-info")
async def edit_info(seller: schemas.UpdateSellerInfo, request: Request, user=Depends(manager)):
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    status = 1
    message = ""

    updated_info = seller_crud.update_seller_by_account_id(db=db, seller=seller, account_id=account_id)

    if updated_info:
        status = 1
        message = "Cập nhật thành công"
    else:
        status = 0
        message = "Cập nhật không thành công. Thử lại sau!"

    return {"status": status, "message": message}

@router.put("/profile/edit-account")
async def edit_account(account: schemas.UpdateAccountName, request: Request, user=Depends(manager)):
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    status = 1
    message = ""
    # Dữ liệu tên đăng nhập gửi qua từ form
    username = account.account_username

    updated_username = account_crud.update_account_name(db=db, account=account, account_id=account_id)

    if updated_username:
        if updated_username == username:
            status = 1
            message = "Cập nhật thành công"
        else:
            status = 0
            message = "Cập nhật không thành công. "
    else:
        status = 0
        message = "Cập nhật không thành công. Thử lại sau"

    return {"status": status, "message": message}

@router.get("/food", response_class=HTMLResponse)
def read_profile_seller(request: Request, page: int = 1, query: Union[str, None] = None, user=Depends(manager)):
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    # Data cần sử dụng
    account_id = user.account_id
    username = user.account_username
    db_ = get_database_session()
    # -------------------------------------------------------------
    count = food_crud.count_all_foods_by_account(db=db_, account_id=account_id, query=query)
    # print(f"Count: {count}")
    # print(f"Type Count: {type(count)}") => List
    
    # print(f"Count 1: {count[0]}") 
    # print(f"Count 1: {type(count[0])}") => sqlalchemy.engine.row.Row

    print(f"Count: {count[0]['TOTAL_ROW']}") 
    #-----------------------------------------------------------------

    # Phân trang
    # Trong đó page là trang hiện tại
    limit = 5   #Số dòng muốn show
    offset = (page - 1)*limit
    TOTAL_ROW = count[0]['TOTAL_ROW'] # => Lấy tổng số dòng
    TOTAL_PAGE = math.ceil(TOTAL_ROW/limit) # => Tổng số trang
    first_page = 'disabled' if page == 1 else ''
    last_page = ''
    if TOTAL_PAGE == 0:
        last_page = 'disabled' 
    elif page == TOTAL_PAGE:
        last_page = 'disabled'
    next_page = page + 1
    previous_page = page - 1

    # Lấy loại thức ăn
    food_type_info = food_type_crud.get_all_food_type(db=db_, skip=0, limit=100)

    food_type_data = []
    for food_type in food_type_info:
        food_type_data.append(food_type.__dict__)
    
    # Lấy danh sách thức ăn của nhà hàng thuộc seller thuộc tài khoản
    
    food_info = food_crud.get_all_foods_by_account(db=db_, account_id=account_id, query=query, skip=offset, limit=limit)
    
    food_data = []
    for food in food_info:
        food_data.append(food)

    print(food_data)

    data_res = {
        "request": request,
        "title": 'Thông tin Seller',
        'username': username,
        'account_id': account_id,
        'food_type_info': food_type_data,
        'food_info': food_data,
        'TOTAL_ROW': TOTAL_ROW,
        'TOTAL_PAGE': TOTAL_PAGE,
        'page': page,
        'first_page': first_page,
        'last_page': last_page,
        'next_page': next_page,
        'previous_page': previous_page,
        'query': query
    }
    return templates.TemplateResponse("seller_list_food.html", data_res)

@router.get("/check-duplicate-username")
def check_duplicate_username(username: str):
    count = account_crud.count_duplicate_username(db=db, username=username)

    return {"TOTAL_ROW": count[0]['TOTAL']}

@router.get("/food/fetch-total-row")
def fetch_total_row_food(request: Request, query: Union[str, None] = None, user=Depends(manager)):
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    # Data cần sử dụng
    db_ = get_database_session()
    account_id = user.account_id
    username = user.account_username
    count = food_crud.count_all_foods_by_account(db=db_, account_id=account_id, query=query)
    TOTAL_ROW = count[0]['TOTAL_ROW'] 

    return {"TOTAL_ROW": TOTAL_ROW}

# Dashboard ----------------------------------------------------------------------
@router.get("/fetch-total-rows-food")
def fetch_total_rows_food(request: Request, user = Depends(manager)):
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    # Lấy tổng số món ăn của tài khoản này
    db_ = get_database_session()
    account_id = user.account_id
    count = food_crud.get_total_rows_food(db=db_, account_id=account_id)
    TOTAL_ROWS_FOOD = count[0]['TOTAL_ROW_FOOD']

    print(f"count: {count}")
    print(f"total: {TOTAL_ROWS_FOOD}")

    return {"TOTAL_ROWS_FOOD": TOTAL_ROWS_FOOD}

@router.get("/fetch-total-rows-order")
def fetch_total_rows_order(request: Request, user = Depends(manager)):
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    # Lấy tổng số đơn hàng của tài khoản này
    db_ = get_database_session()
    account_id = user.account_id
    count = order_crud.get_total_rows_order(db=db_, account_id=account_id)
    TOTAL_ROWS_ORDER = count[0]['TOTAL_ROW_ORDER']

    print(f"count: {count}")
    print(f"total: {TOTAL_ROWS_ORDER}")

    return {"TOTAL_ROWS_ORDER": TOTAL_ROWS_ORDER}

@router.delete("/delete-food")
def delete_food(food_id: int, request: Request, user = Depends(manager)):


    # Tạo biến phản hồi
    status = 1
    message = ""

    # Xóa món ăn ở warehouse trước
    num_row_deleted = food_crud.delete_food_in_warehouse(db=db, food_id=food_id)

    if num_row_deleted > 0:
        num_row_food_deleted = food_crud.delete_food(db=db, food_id=food_id)
        if num_row_food_deleted > 0:
            status = 1
            message = "Xóa món ăn thành công"
        else:
            status = 0
            message = "Xóa món ăn không thành công"
    else:
        status = 0
        message = "Lỗi khi xóa ở warehouse"

    return {"status": status, "message": message}

@router.get("/orders", response_class=HTMLResponse)
def order_list(request: Request, user=Depends(manager)):
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    # Data cần sử dụng
    account_id = user.account_id
    username = user.account_username

    data_res = {
        "request": request,
        "title": "Trang đơn hàng",
        'username': username,
        'account_id': account_id
    }
    return templates.TemplateResponse("seller_order_list.html", data_res)
    

@router.get("/", response_class=HTMLResponse)
def seller_index_page( request: Request, user = Depends(manager)):
    if user.account_type != 2:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    username = user.account_username

    #Lấy thông tin tài khoản
    db_ = get_database_session()
    seller_info = seller_crud.get_seller_by_account_id(db=db_, account_id=account_id)

    # Lấy danh sách món ăn hết hàng
    list_foods_out_of_stock = food_crud.get_list_foods_out_of_stock(db=db_, account_id=account_id)

    print(f"out of stock: {list_foods_out_of_stock}")

    data = []
    data.append(seller_info.__dict__)
    data_res = {
        "request": request,
        "title": 'Thông tin Seller',
        'seller_info': data,
        'username': username,
        'account_id': account_id,
        'list_foods_out_of_stock': list_foods_out_of_stock
    }
    return templates.TemplateResponse("seller_index.html", data_res)


@router.get("/{id}")
def read_seller(id: int, db: Session = Depends(get_database_session)):
    seller = seller_crud.get_seller(db,id)
    
    return seller