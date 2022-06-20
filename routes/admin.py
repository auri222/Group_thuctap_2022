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
from crud import admin_crud, account_crud
from routes.login import manager
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

@router.get("/profile/{account_id}", response_class=HTMLResponse)
def read_profile_admin(account_id: int, request: Request, user=Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    
    admin_info = admin_crud.get_admin_by_account_id(db=db, account_id=account_id)
    account_info = account_crud.get_account(db, account_id=account_id)
    username = account_info.account_username
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

@router.get("/{account_id}", response_class=HTMLResponse)
def admin_page(account_id: int, request: Request, user = Depends(manager)):
    if user.account_type != 1:
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': 'Bạn không được cấp quyền để vào trang này!'
        }
        return templates.TemplateResponse("login.html", error_data)

    admin_info = admin_crud.get_admin_by_account_id(db=db, account_id=account_id)
    account_info = account_crud.get_account(db, account_id=account_id)
    username = account_info.account_username
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

@router.put("/update/{id}")
def update_admin(id: int, admin: schemas.Admin):
    return admin_crud.update_admin(db, admin=admin, admin_id=id)

@router.delete("/delete/{id}")
def delete_admin(id: int):
    return admin_crud.delete_admin(db, admin_id=id)

