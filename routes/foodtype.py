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
from crud import food_type_crud
from routes.login import manager
router = APIRouter(
    prefix="/foodtype",
    tags=['Foodtypes']
)
def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()

templates = Jinja2Templates(directory="public")

@router.get('/')
def get_foodtype(id: int):
    foodtype_info = food_type_crud.get_food_type_by_ID(db=db, foodtype_ID=id)
    return foodtype_info

@router.get('/all')
def get_all_foodtypes(skip: int, limit: int):
    foodtypes = food_type_crud.get_all_food_type(db, skip=skip, limit=limit)
    return foodtypes

@router.post('/create')
def create_foodtype(foodtype: schemas.FoodType):
    db_foodtype = food_type_crud.create_food_type(db=db, foodtype=foodtype)

    return db_foodtype

@router.put('/update')
def update_foodtype(foodtype_id: int, foodtype: schemas.FoodType):
    db_foodtype = food_type_crud.update_food_type(db=db, foodtype=foodtype, foodtype_ID=foodtype_id)
    updated_id = db_foodtype.food_type_id
    updated_foodtype = food_type_crud.get_food_type_by_ID(db=db, foodtype_ID=updated_id)
    return updated_foodtype

@router.delete('/delete')
def delete_foodtype(foodtype_id: int):
    return food_type_crud.delete_food_type(db=db, foodtype_ID=foodtype_id)