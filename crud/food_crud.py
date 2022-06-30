from sqlalchemy.orm import Session
import models
import schemas

def get_all_foods(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Food).offset(skip).limit(limit).all()

def get_food_from_account(db: Session, account_id: int, skip: int = 0, limit: int = 100):
    result = db.execute(f"""SELECT acc.account_id AS account_ID, sl.seller_id AS seller_ID, res.restaurant_id AS restaurant_ID, f.*, rw.food_quantity
FROM restaurant_warehouse rw
JOIN restaurant res ON res.restaurant_id = rw.restaurant_id
JOIN seller sl ON sl.seller_id = res.seller_id
JOIN account acc ON acc.account_id = sl.account_id
JOIN food f ON f.food_id = rw.food_id
WHERE acc.account_id = {account_id}""")
    return result.fetchall()

def create_food_info(db: Session, food: schemas.Food):
    db_food = models.Food(  food_name = food.food_name,
                            food_image = food.food_image,
                            food_price = food.food_price,
                            food_description = food.food_description,
                            food_type_id = food.food_type_id)
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

def create_food_info_return_ID(db: Session, food: schemas.CreateFoodInfo):
    db_food = models.Food(  food_name = food.food_name,
                            food_image = food.food_image,
                            food_price = food.food_price,
                            food_description = food.food_description,
                            food_type_id = food.food_type_id)
    db.add(db_food)
    db.commit()
    food_id = db_food.food_id
    db.refresh(db_food)
    return food_id

def get_food_info_by_ID(db: Session, food_id: int):
    food = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    
    return food

def update_food_info(db: Session, food: schemas.UpdateFoodInfo, food_id: int):
    db_food = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    db_food.food_name = food.food_name
    db_food.food_price = food.food_price
    db_food.food_description = food.food_description
    db_food.food_type_id = food.food_type_id
    db.commit(db_food)
    updated_id =  db_food.food_id
    return updated_id

def update_food_image(db: Session, food: schemas.UpdateFoodImage, food_id: int):
    db_food = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    db_food.food_image = food.food_image

    db.commit()
    updated_id =  db_food.food_id
    return updated_id

def delete_food(db: Session, food_id: int):
    db_food = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    if db_food is None:
        return {"Error": f"Food with ID {food_id} is not exists"}
    db.delete(db_food)
    db.commit()
    return {"Success": "Delete food successfully"}
