import imp
from config.db import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import RedirectResponse, JSONResponse
from datetime import timedelta
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
from ultilities import Hash
from crud import account_crud
import models, schemas
router = APIRouter(tags=['Auth_Login'])

templates = Jinja2Templates(directory="public")



def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()

secret = os.urandom(24).hex()
SECRET = secret
token_url = "/auth/login"
manager = LoginManager(SECRET,token_url,use_cookie=True)
manager.cookie_name = "access-token"

@router.get("/login_form", response_class=HTMLResponse)
def login_form(request: Request):
    login_form = {
        "request": request,
        "title": 'Form đăng nhập seller'
    }
    return templates.TemplateResponse("login.html", login_form)



@manager.user_loader()
def load_user(username:str):
    db_ = get_database_session()
    user = account_crud.get_account_by_name(db_, username)
    return user

@router.post("/auth/login")
async def login( request: Request, username: str = Form(...), password: str = Form(...)):
    

    print(username)
    print(password)
    user = load_user(username)
    if not user:
        error = f"Không tìm thấy người dùng với tên đăng nhập là {username}"
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': error,
            'username': username
        }
        return templates.TemplateResponse("login.html", error_data)

    elif not Hash.verify(password,user.account_password):
        error_data = {
            "request": request,
            "title": 'Trang đăng nhập',
            'error': "Mật khẩu chưa đúng!",
            'username': username
        }
        return templates.TemplateResponse("login.html", error_data)
    
    access_token = manager.create_access_token(data = dict(sub=username), expires=timedelta(hours=1)
    )
    account_type = user.account_type
    account_id = user.account_id

    # Đúng thông tin đăng nhập thì set status = 1
    active_status = account_crud.update_account_active_status(db=db, account_id=account_id, status=1)
    print(f"active status: {active_status}")

    if account_type == 1:
        url = f"/admin/"
        resp = RedirectResponse(url=url,status_code=status.HTTP_302_FOUND)
    
    if account_type == 2:
        url = f"/seller/"
        resp = RedirectResponse(url=url,status_code=status.HTTP_302_FOUND)
    
    if account_type == 3:
        url = f"/buyer/"
        resp = RedirectResponse(url=url,status_code=status.HTTP_302_FOUND)
    
    
    manager.set_cookie(resp,access_token)
    
    return resp

@router.get("/private")
def getPrivateendpoint(username=Depends(manager)):
    return "You are an authentciated user"

@router.get('/logout', response_class=HTMLResponse)
def protected_route(request: Request, user=Depends(manager)):
    account_id = user.account_id

    # Đúng thông tin đăng nhập thì set status = 1
    active_status = account_crud.update_account_active_status(db=db, account_id=account_id, status=0)
    print(f"active status: {active_status}")
    resp = RedirectResponse(url="/login_form", status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp, "")
    return resp

