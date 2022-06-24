from sqlalchemy.orm import Session
import models
import schemas

def get_all_food_type(db: Session, skip: int = 0, limit: int = 100): 
    return db.query(models.FoodType).offset(skip).limit(limit).all()

def get_food_type_by_ID(db: Session, foodtype_ID: int):
    db_foodtype = db.query(models.FoodType).filter(models.FoodType.food_type_id == foodtype_ID).first()
    if db_foodtype is None:
        return {"Error": f"Food type of this ID {foodtype_ID} is not exists"}
    return db_foodtype

def get_food_type_by_name(db: Session, foodtype_name: str):
    db_foodtype = db.query(models.FoodType).filter(models.FoodType.food_type_name == foodtype_name).first()
    if db_foodtype is None:
        return {"Error": f"{foodtype_name} is not exists"}
    return db_foodtype

def count_food_type(db: Session, foodtype_name: str):
    return db.query(models.FoodType).filter(models.FoodType.food_type_name == foodtype_name).count()

def create_food_type(db: Session, foodtype: schemas.FoodType):
    db_foodtype = models.FoodType(food_type_name = foodtype.food_type_name)
    db.add(db_foodtype)
    db.commit()
    db.refresh(db_foodtype)
    return db_foodtype

def update_food_type(db: Session, foodtype: schemas.FoodType, foodtype_ID: int):
    db_foodtype = db.query(models.FoodType).filter(models.FoodType.food_type_id == foodtype_ID).first()
    if db_foodtype is None:
        return {"Error": f"Food type of this ID {foodtype_ID} is not exists"}
    db_foodtype.food_type_name = foodtype.food_type_name
    db.commit()
    db_foodtype_id = db_foodtype.food_type_id
    return db_foodtype_id

def delete_food_type(db: Session, foodtype_ID: int):
    db_foodtype = db.query(models.FoodType).filter(models.FoodType.food_type_id == foodtype_ID).first()
    if db_foodtype is None:
        return {"Error": f"Food type of this ID {foodtype_ID} is not exists"}
    db.delete(db_foodtype)
    db.commit()
    return {"Success": "Delete food type successfully"}

