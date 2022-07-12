from email import message
from re import template
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
from crud import admin_crud, account_crud, food_type_crud, payment_crud, seller_crud, buyer_crud
from routes.login import manager
import math
router = APIRouter(
    prefix="/admin",
    tags=['Admins']
)
def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()

templates = Jinja2Templates(directory="public")

@router.post("/create/")
def create_admin(acc_id: int, admin: schemas.CreateAdminInfo):
    return admin_crud.create_admin_info(db, admin=admin, account_id=acc_id)

@router.get("/get-all/")
def read_admins(skip: int = 0, limit: int=100):
    admins = admin_crud.get_all_admins(db, skip=0, limit=10)
    return admins

@router.get("/profile/", response_class=HTMLResponse)
def read_profile_admin(request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    username = user.account_username
    admin_info = admin_crud.get_admin_by_account_id(db=db, account_id=account_id)
    account_info = account_crud.get_account(db, account_id=account_id)

    data = []
    data.append(admin_info.__dict__)
    data_res = {
        "request": request,
        "title": 'Thông tin Admin',
        'admin_info': data,
        'username': username,
        'account_id': account_id
    }
    return templates.TemplateResponse("admin_profile.html", data_res)

@router.get("/", response_class=HTMLResponse)
def admin_page(request: Request, user = Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)
    account_id = user.account_id
    username = user.account_username
    admin_info = admin_crud.get_admin_by_account_id(db=db, account_id=account_id)
    account_info = account_crud.get_account(db, account_id=account_id)

    data = []
    data.append(admin_info.__dict__)
    data_res = {
        "request": request,
        "title": 'Thông tin Admin',
        'admin_info': data,
        'username': username,
        'account_id': account_id
    }
    return templates.TemplateResponse("admin_index.html", data_res)

@router.put("/update/")
def update_admin(id: int, admin: schemas.Admin):
    return admin_crud.update_admin(db, admin=admin, admin_id=id)

@router.delete("/delete/")
def delete_admin(id: int):
    return admin_crud.delete_admin(db, admin_id=id)

@router.get("/edit_profile", response_class=HTMLResponse)
def edit_admin_form(account_id: int,request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    admin_info = admin_crud.get_admin_by_account_id(db=db,account_id=account_id)
    account_info = account_crud.get_account(db, account_id=account_id)
    username = account_info.account_username
    error = ""
    data = []
    if admin_info:
        data.append(admin_info.__dict__)
        error = None
    else:
        error = "Không có dữ liệu"    
    
    data_res = {
        "request": request,
        "title": 'Thông tin tài khoản Admin',
        'username': username,
        'account_id': account_id,
        'admin_info': data,
        'error': error   
    }
    return templates.TemplateResponse("admin_edit_profile.html", data_res)


@router.put("/edit_profile")
def edit_admin_info(account_id: int, admin: schemas.UpdateAdminInfo, request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    
    admin_info = admin_crud.update_admin(db=db, admin=admin, admin_id=account_id )
    print(f"admin info: {admin_info}")
    if admin_info:
        status = 1
        message = "Sửa thành công"
    else:
        status = 0
        message = "Sửa không thành công. Thử lại sau!"
    

    return {"status": status,"message": message, "account_id": account_id}

@router.get("/edit_account", response_class=HTMLResponse)
def edit_admin_form(account_id: int,request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_info = account_crud.get_account(db, account_id=account_id)
    username = account_info.account_username
    error = ""
    data = []
    if account_info:
        data.append(account_info.__dict__)
        error = None
    else:
        error = "Không có dữ liệu"    
    
    data_res = {
        "request": request,
        "title": 'Thông tin tài khoản Admin',
        'username': username,
        'account_id': account_id,
        'account_info': data,
        'error': error   
    }
    return templates.TemplateResponse("admin_edit_account.html", data_res)


@router.put("/edit_account")
def edit_admin_info(account_id: int, update_pass: schemas.UpdateAccountPassword, request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)
    

    account_id = account_crud.update_account_password(db=db,account=update_pass,account_id=account_id)
    if account_id != None:
        status = 1
        message = "Sửa tài khoản thành công!"
    else:
        status = 0
        message = "Hệ thống lỗi! Vui lòng thử lại sau!"
    

    return {"status": status,"message": message, "account_id": account_id}

@router.get("/foodtype/", response_class=HTMLResponse)
def read_foodtype(request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    username = user.account_username
    foodtype_info = food_type_crud.get_all_food_type(db=db, skip=0, limit=10)

    error = ""
    if foodtype_info:
        error = None
    else: 
        error = "Không có dữ liệu"
    print(error)
    print(foodtype_info)
    data = []
    for foodtype in foodtype_info:
        data.append(foodtype.__dict__)
    print(f"food type info {data}")
    data_res = {
        "request": request,
        "title": 'Thông tin Admin',
        'username': username,
        'account_id': account_id,
        'foodtype_info': data,
        'error': error
    }
    return templates.TemplateResponse("admin_foodtype.html", data_res)

@router.get("/foodtype/create", response_class=HTMLResponse)
def create_foodtype_form(request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    username = user.account_username
    
    data_res = {
        "request": request,
        "title": 'Thông tin Admin',
        'username': username,
        'account_id': account_id   
    }
    return templates.TemplateResponse("admin_foodtype_create.html", data_res)

@router.post("/foodtype/create")
def create_food_type(foodtype: schemas.FoodType):
    print(foodtype)
    #Khởi tạo biến thông báo
    status = 1
    message = ""

    db_foodtype = food_type_crud.create_food_type(db=db, foodtype=foodtype)
    
    if db_foodtype:
        status = 1
        message = "Thêm thông tin thành công"
    else:
        status = 0
        message = "Lỗi. Thử lại sau"
    
    return {"status": status, "message": message}


@router.get("/foodtype/edit", response_class=HTMLResponse)
def edit_foodtype_form(foodtype_id: int,request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    username = user.account_username

    foodtype_info = food_type_crud.get_food_type_by_ID(db=db, foodtype_ID=foodtype_id)

    data = []
    if foodtype_info:
        data.append(foodtype_info.__dict__)
        error = None
    else:
        error = "Không có dữ liệu"    
    
    
    data_res = {
        "request": request,
        "title": 'Thông tin Admin',
        'username': username,
        'account_id': account_id,
        'foodtype_info': data,
        'error': error   
    }
    return templates.TemplateResponse("admin_foodtype_edit.html", data_res)

@router.put("/foodtype/edit")
def edit_foodtype(foodtype_id: int, foodtype: schemas.FoodType, request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id

    #Kiểm tra nếu tên nhập trùng
    foodtype_name = foodtype.food_type_name
    row_count = food_type_crud.count_food_type(db=db, foodtype_name=foodtype_name)
    status = 1
    message = ""
    print(f"Số tên trùng: {row_count}")
    if row_count > 0:
        status = 0
        message = "Tên loại thức ăn bị trùng!"
    else:
        foodtype_info = food_type_crud.update_food_type(db=db, foodtype=foodtype, foodtype_ID=foodtype_id)
        print(f"Food type info: {foodtype_info}")
        if foodtype_info:
            status = 1
            message = "Sửa thành công"
        else:
            status = 0
            message = "Sửa không thành công. Thử lại sau!"

    

    return {"status": status, "message": message, "account_id": account_id}
        
@router.get("/payment_method/", response_class=HTMLResponse)
def read_payment_method(request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    username = user.account_username
    payment_method = payment_crud.get_all_payment_method(db=db, skip=0, limit=10)

    error = ""
    if payment_method:
        error = None
    else: 
        error = "Không có dữ liệu"
    print(error)
    print(payment_method)
    data = []
    for payment in payment_method:
        data.append(payment.__dict__)
    print(f"payment info {data}")
    data_res = {
        "request": request,
        "title": 'Phương thức thanh toán',
        'username': username,
        'account_id': account_id,
        'payment_info': data,
        'error': error
    }
    return templates.TemplateResponse("admin_payment.html", data_res)
    

@router.get("/payment_method/create", response_class=HTMLResponse)
def create_payment_form(request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    username = user.account_username
    
    data_res = {
        "request": request,
        "title": 'Phương thức thanh toán',
        'username': username,
        'account_id': account_id   
    }
    return templates.TemplateResponse("admin_payment_create.html", data_res)

@router.post("/payment_method/create")
def create_food_type(payment_method: schemas.PaymentMethod):
    #Khởi tạo biến thông báo
    status = 1
    message = ""

    db_payment_method = payment_crud.create_payment_method(db=db,payment_method=payment_method)
    
    if db_payment_method:
        status = 1
        message = "Thêm thông tin thành công"
    else:
        status = 0
        message = "Lỗi. Thử lại sau"
    
    return {"status": status, "message": message}

@router.get("/payment_method/edit", response_class=HTMLResponse)
def edit_payment_form(payment_id: int,request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    username = user.account_username

    payment_info = payment_crud.get_payment_method_by_ID(db=db, payment_id=payment_id)

    data = []
    if payment_info:
        data.append(payment_info.__dict__)
        error = None
    else:
        error = "Không có dữ liệu"    
    
    
    data_res = {
        "request": request,
        "title": 'Phương thức thanh toán',
        'username': username,
        'account_id': account_id,
        'payment_info': data,
        'error': error   
    }
    return templates.TemplateResponse("admin_payment_edit.html", data_res)

@router.put("/payment_method/edit")
def edit_payment_method(payment_id: int, payment_method: schemas.PaymentMethod, request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id

    #Kiểm tra nếu tên nhập trùng
    payment_method_name = payment_method.payment_method_name
    row_count = payment_crud.count_payment_method(db=db,payment_method_name=payment_method_name)
    status = 1
    message = ""
    print(f"Số tên trùng: {row_count}")
    if row_count > 0:
        status = 0
        message = "Tên phương thức thanh toán bị trùng!"
    else:
        payment_info = payment_crud.update_payment_method(db=db,payment_method=payment_method, payment_id=payment_id)
        print(f"Food type info: {payment_info}")
        if payment_info:
            status = 1
            message = "Sửa thành công"
        else:
            status = 0
            message = "Sửa không thành công. Thử lại sau!"

    db_ = get_database_session()

    count = admin_crud.count_all_seller_accounts(db=db_)
    TOTAL_ROWS_SELLER = count[0]['TOTAL_ROW_SELLER']

    return {"TOTAL_ROWS_SELLER": TOTAL_ROWS_SELLER }

@router.get("/fetch-all-rows-seller")
def fetch_all_rows_seller(request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    db_ = get_database_session()

    count = admin_crud.count_all_seller_accounts(db=db_)
    TOTAL_ROWS_SELLER = count[0]['TOTAL_ROW_SELLER']

    return {"TOTAL_ROWS_SELLER": TOTAL_ROWS_SELLER }

@router.get("/fetch-all-rows-buyer")
def fetch_all_rows_buyer(request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    db_ = get_database_session()

    count = admin_crud.count_all_buyer_accounts(db=db_)
    TOTAL_ROWS_BUYER = count[0]['TOTAL_ROW_BUYER']

    return {"TOTAL_ROWS_BUYER": TOTAL_ROWS_BUYER }

@router.get("/fetch-all-rows-order")
def fetch_all_rows_order(request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    db_ = get_database_session()

    count = admin_crud.count_all_orders(db=db_)
    TOTAL_ROWS_ORDER = count[0]['TOTAL_ROW_ORDER']

    return {"TOTAL_ROWS_ORDER": TOTAL_ROWS_ORDER}
# ------------------------------------------------------------------------------------------

# Quan ly danh sach seller
@router.get("/sellers", response_class=HTMLResponse)
def get_all_sellers(request: Request, page: int=1, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    username = user.account_username

    db_ = get_database_session()

    count = seller_crud.count_all_rows_seller(db=db_)

    # Phân trang
    limit = 5 #1 trang 5 dòng
    offset = (page - 1)*limit
    TOTAL_ROWS = count[0]['TOTAL_ROW']
    TOTAL_PAGES = math.ceil(TOTAL_ROWS/limit)
    first_page = 'disabled' if page == 1 else ''
    last_page = ''
    if TOTAL_PAGES == 0:
        last_page = 'disabled'
    elif page == TOTAL_PAGES:
        last_page = 'disabled'

    next_page = page + 1
    previous_page = page - 1

    #Lấy dữ liệu 
    sellers_info = seller_crud.get_all_sellers(db=db_, skip=offset, limit=limit)

    seller_data = []
    for seller in sellers_info:
        seller_data.append(seller)

    data_res = {
        "request": request,
        "title": 'Danh sách người bán',
        'username': username,
        'account_id': account_id,
        'sellers_info': seller_data,
        'first_page': first_page,
        'last_page': last_page,
        'next_page': next_page,
        'previous_page': previous_page,
        'TOTAL_ROW': TOTAL_ROWS,
        'TOTAL_PAGE': TOTAL_PAGES,
        'page': page
    }

    return templates.TemplateResponse("admin_sellers_list.html", data_res)

# Quan ly danh sach buyer
@router.get("/buyers", response_class=HTMLResponse)
def get_all_buyers(request: Request, page: int=1, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    username = user.account_username

    db_ = get_database_session()

    count = buyer_crud.count_all_rows_buyer(db=db_)

    # Phân trang
    limit = 5 #1 trang 5 dòng
    offset = (page - 1)*limit
    TOTAL_ROWS = count[0]['TOTAL_ROW']
    TOTAL_PAGES = math.ceil(TOTAL_ROWS/limit)
    first_page = 'disabled' if page == 1 else ''
    last_page = ''
    if TOTAL_PAGES == 0:
        last_page = 'disabled'
    elif page == TOTAL_PAGES:
        last_page = 'disabled'

    next_page = page + 1
    previous_page = page - 1

    #Lấy dữ liệu 
    buyers_info = buyer_crud.get_all_buyers(db=db_, skip=offset, limit=limit)

    buyer_data = []
    for buyer in buyers_info:
        buyer_data.append(buyer)

    data_res = {
        "request": request,
        "title": 'Danh sách người bán',
        'username': username,
        'account_id': account_id,
        'buyers_info': buyer_data,
        'first_page': first_page,
        'last_page': last_page,
        'next_page': next_page,
        'previous_page': previous_page,
        'TOTAL_ROW': TOTAL_ROWS,
        'TOTAL_PAGE': TOTAL_PAGES,
        'page': page
    }

    return templates.TemplateResponse("admin_buyers_list.html", data_res)

@router.get("/fetch-buyer-info")
def fetch_buyer_info(buyer_id: int, request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    db_ = get_database_session()
    buyer_info = buyer_crud.get_all_info_buyer(db=db_, buyer_id=buyer_id)

    return {"buyer_info": buyer_info}
    
@router.get("/fetch-seller-info")
def fetch_seller_info(seller_id: int, request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    db_ = get_database_session()
    seller_info = seller_crud.get_all_info_seller(db=db_, seller_id=seller_id)


    return {"seller_info": seller_info}

@router.delete("/payment_method/delete")
def edit_payment_method(payment_id: int, request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    account_id = user.account_id
    payment_info = payment_crud.delete_payment_method(db=db, payment_id=payment_id)
    print(f"Payment method: {payment_info}")
    if payment_info:
        status = 1
        message = "Xóa thành công"
    else:
        status = 0
        message = "Xóa không thành công. Thử lại sau!"

    

    return {"status": status, "message": message, "account_id": account_id}
