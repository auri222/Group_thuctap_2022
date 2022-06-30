from fastapi import FastAPI, Depends, Request,Response,Form
import models, schemas
from config.db import engine, SessionLocal
from sqlalchemy.orm import Session
from routes import admin, account, login, register, buyer, seller, foodtype, restaurant, food
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from routes.login import manager
from fastapi.responses import RedirectResponse
from starlette.responses import JSONResponse,RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates
from crud import restaurant_crud, food_crud
import uvicorn
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="public")

app.mount('/static', app=StaticFiles(directory="static"), name="static")

def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

app.include_router(login.router)
app.include_router(register.router)
app.include_router(account.router)
app.include_router(admin.router)
app.include_router(seller.router)
app.include_router(buyer.router)
app.include_router(foodtype.router)
app.include_router(restaurant.router)
app.include_router(food.router)


@app.get("/", response_class=HTMLResponse, tags=["Homepage"])
def root(request: Request):

    db_ = get_database_session()

    restaurant_info = restaurant_crud.get_all_restaurants(db=db_, skip=0, limit=10)

    restaurant_data = []
    for info in restaurant_info:
        restaurant_data.append(info)
    print(restaurant_data)
    data_res = {
        "request": request,
        "title": "Trang chủ",
        'restaurant_info': restaurant_data
    }

    return templates.TemplateResponse("buyer_index.html",data_res)

# #bắt phải đăng nhập 
# class NotAuthenticatedException(Exception):
#     pass

# # these two argument are mandatory
# def exc_handler(request, exc):
#     return RedirectResponse(url='/error_auth')

# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request: Request, exc: StarletteHTTPException):
#     return RedirectResponse(url='/error_auth')
#     data_res = {
#         "request": request,
#     }
#     return templates.TemplateResponse("/404.html",data_res)

# manager.not_authenticated_exception = NotAuthenticatedException
# # You also have to add an exception handler to your app instance
# app.add_exception_handler(NotAuthenticatedException, exc_handler)
# @app.get('/error_auth', response_class=JSONResponse,tags=["account"])
# async def template_login(response:Response):
#     return RedirectResponse(url='/login_form')

# if __name__ == "__main__":
#     uvicorn.run(app=app, host="0.0.0.0", port=8088)

@app.get("/read_restaurants", tags=['Root'])
def get_all_restaurant_info():
    db = get_database_session()
    return restaurant_crud.get_all_restaurants(db=db, skip=0, limit=100)