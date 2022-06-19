from config import db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Request, Depends, status, Form
from fastapi.responses import RedirectResponse
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
from ultilities import Hash
from crud import account_crud

router = APIRouter(tags=['Auth_Login'])

# router.mount("/public", StaticFiles(directory="./public"), name="public")
# router.mount("/assets", StaticFiles(directory="./assets"), name="assets")
# templates = Jinja2Templates(directory="./public")



db = db.get_database_session
secret = os.urandom(24).hex()
SECRET = secret
token_url = "/auth/login"
manager = LoginManager(SECRET,token_url,use_cookie=True)
manager.cookie_name = "access-token"

@router.get("/login_form/", response_class=HTMLResponse)
def login_form(request: Request):
    login_form = {
        "request": request,
        "title": 'Form đăng nhập seller',
        'current_page': 0
    }
    return templates.TemplateResponse("/login.html", login_form)

@manager.user_loader()
def load_user(username:str):
    user = account_crud.get_account_by_name(db, account_name=username)
    return user

@router.post("/auth/login")
def login(UserName: str = Form(...), Password: str = Form(...)):
    
    username = UserName
    password = Password
    print(username)
    print(password)
    user = load_user(username)
    if not user:
        raise InvalidCredentialsException
    elif not Hash.verify(password,user.Account_Password):
        raise InvalidCredentialsException
    access_token = manager.create_access_token(data = dict(sub=username)
    )
    print(access_token)
    resp = RedirectResponse(url="/private",status_code=status.HTTP_302_FOUND)
    manager.set_cookie(resp,access_token)
    
    return resp

@router.get("/private")
def getPrivateendpoint(username=Depends(manager)):
    return "You are an authentciated user"