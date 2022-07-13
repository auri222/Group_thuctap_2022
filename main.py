from typing import Union
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
import math
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


# Chưa login ---------------------------------------------------------------------------
# Trang chủ
@app.get("/", response_class=HTMLResponse, tags=["Homepage"])
def root(request: Request):

    db_ = get_database_session()

    restaurant_info = restaurant_crud.get_random_restaurant(db=db_, limit=4)

    restaurant_data = []
    for info in restaurant_info:
        restaurant_data.append(info)
    print(restaurant_data)
    data_res = {
        "request": request,
        "title": "Trang chủ",
        'restaurant_info': restaurant_data
    }

    return templates.TemplateResponse("index.html",data_res)

@app.get("/restaurants", response_class=HTMLResponse, tags=["Homepage"])
def root(request: Request):

    db_ = get_database_session()
    
    # Lấy dữ liệu để phân trang
    count = restaurant_crud.count_all_restaurants(db=db_)
    TOTAL_ROWS = count[0]['TOTAL_RESTAURANT']
    offset = 0
    limit = TOTAL_ROWS

    restaurant_info = restaurant_crud.get_all_restaurants(db=db_, skip=offset, limit=limit)

    restaurant_data = []
    for info in restaurant_info:
        restaurant_data.append(info)
    print(restaurant_data)
    data_res = {
        "request": request,
        "title": "Trang chủ",
        'restaurant_info': restaurant_data
    }

    return templates.TemplateResponse("restaurant_list.html",data_res)

@app.get("/restaurant_detail", response_class=HTMLResponse, tags=["Restaurant Detail"])
def restaurant_detail(restaurant_id: int, request: Request, page: int=1, query: Union[str, None]=None):
    # Lấy phiên làm việc database
    db_ = get_database_session()

    # Lấy tổng số dòng món ăn
    count = food_crud.get_total_rows_food_by_restaurant_id(db=db_, restaurant_id=restaurant_id, query=query)

    # Phân trang
    limit = 6
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

    # Lấy thông tin nhà hàng dựa trên ID
    restaurant_data = restaurant_crud.restaurant_info_for_restaurant_index(db=db_, restaurant_id=restaurant_id)

    # Lấy danh sách món ăn dựa trên ID nhà hàng
    food_info = food_crud.get_all_rows_food_by_restaurant_id(db=db_, restaurant_id=restaurant_id, query=query, skip=offset, limit=limit)
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
        'restaurant_info': restaurant_data,
        'restaurant_id': restaurant_id,
        'food_info': food_data,
        'food_type_info': food_type_data,
        'first_page': first_page,
        'last_page': last_page,
        'next_page': next_page,
        'previous_page': previous_page,
        'query': query,
        'TOTAL_ROW': TOTAL_ROWS,
        'TOTAL_PAGE': TOTAL_PAGES,
        'page': page
    }
    return templates.TemplateResponse("restaurant_index.html", data_res)

# ----------------------------------------------------------------------------------------------------------

# if __name__ == "__main__":
#     uvicorn.run(app=app, host="0.0.0.0", port=8088)

@app.get("/read_restaurants", tags=['Root'])
def get_all_restaurant_info():
    db = get_database_session()
    return restaurant_crud.get_all_restaurants(db=db, skip=0, limit=100)


# #Bắt phải đăng nhập ----------------------------------------------------------------------
class NotAuthenticatedException(Exception):
    pass

# these two argument are mandatory
def exc_handler(request, exc):
    return RedirectResponse(url='/error_auth')

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return RedirectResponse(url='/error_auth')
    # data_res = {
    #     "request": request,
    # }
    # return templates.TemplateResponse("/404.html",data_res)

manager.not_authenticated_exception = NotAuthenticatedException
# You also have to add an exception handler to your app instance
app.add_exception_handler(NotAuthenticatedException, exc_handler)
@app.get('/error_auth', response_class=HTMLResponse, tags=["account"])
async def template_login(request: Request):
    data_res = {
        "request": request,
        'error': 'Bạn chưa đăng nhập'
    }
    return templates.TemplateResponse("login.html", data_res)

# Check if login ---------------------------------------------------------------------------

manager.useRequest(app=app)

@app.get("/check-login")
def check_login(request: Request):
    user = request.state.user
    status = 1
    message = ""

    if user is None:
        status = 0
        message = "Bạn cần đăng nhập để thực hiện chức năng này!"

    return {"status": status, "message": message}

