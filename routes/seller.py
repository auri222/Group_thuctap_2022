from fastapi import APIRouter, Depends, HTTPException, Request, File, Form
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from config.db import SessionLocal
import models, schemas
from crud import seller_crud

router = APIRouter(
    prefix="/seller",
    tags=['Sellers']
)
def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()


@router.get("/all")
def read_sellers(skip: int = 0, limit: int=100):
    sellers = seller_crud.get_sellers(db, skip=skip, limit=limit)
    return sellers

@router.post("/create/{account_id}")
def create_seller(account_id: int, seller: schemas.CreateSellerInfo, db: Session = Depends(get_database_session)):
    return seller_crud.create_seller(db, seller=seller, account_id=account_id)

# @router.post("/create/{account_id}", tags=["create_sellers"])
# def create_seller_return_ID(account_id: int, seller: schemas.CreateSellerInfo, db: Session = Depends(get_database_session)):
#     return seller_crud.create_seller_return_ID(db, seller=seller, account_id=account_id)

@router.delete("/delete/{id}")
def seller_detele(id: int, db: Session = Depends(get_database_session)):
    
    return seller_crud.delete_seller(db,id)

@router.put("/update/")
def seller_update(seller: schemas.Seller, db: Session = Depends(get_database_session)):
    update_sel = seller_crud.update_seller(db,seller=seller)
    return seller_crud.get_seller(db, update_sel)

@router.get("/{id}")
def read_seller(id: int, db: Session = Depends(get_database_session)):
    seller = seller_crud.get_seller(db,id)
    
    return seller

