from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.db import SessionLocal
import models, schemas
from crud import buyer_crud
router = APIRouter(
    prefix="/buyer",
    tags=['Buyers']
)
def get_database_session():
    try:
        db = SessionLocal()
        return db
    finally:
        db.close()

db = get_database_session()

