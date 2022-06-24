from fastapi import FastAPI, Depends
import models, schemas
from config.db import engine
from sqlalchemy.orm import Session
from routes import admin, account, login, register, buyer, seller, foodtype
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount('/static', app=StaticFiles(directory="static"), name="static")


app.include_router(login.router)
app.include_router(register.router)
app.include_router(account.router)
app.include_router(admin.router)
app.include_router(seller.router)
app.include_router(buyer.router)
app.include_router(foodtype.router)