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

# Xóa foodtype --------------------------------------------------------
def fetch_total_row_food(db: Session, food_type_id: int):
    string = f"""SELECT COUNT(*) as TOTAL_FOOD
                FROM food_type ft
                JOIN food f ON f.food_type_id = ft.food_type_id
                JOIN restaurant_warehouse rw ON rw.food_id = f.food_id
                JOIN restaurant res ON res.restaurant_id = rw.restaurant_id
                WHERE ft.food_type_id = {food_type_id}"""

    result = db.execute(string)
    return result.fetchall()

def fetch_restaurant_list(db: Session, food_type_id: int):
    string = f"""SELECT res.restaurant_name
FROM food_type ft
JOIN food f ON f.food_type_id = ft.food_type_id
JOIN restaurant_warehouse rw ON rw.food_id = f.food_id
JOIN restaurant res ON res.restaurant_id = rw.restaurant_id
WHERE ft.food_type_id = {food_type_id}
GROUP BY res.restaurant_name"""
    result = db.execute(string)
    return result.fetchall()

def delete_food_from_warehouse(db: Session, food_type_id: int):
    string = f"""DELETE rw
                FROM restaurant_warehouse rw
                JOIN food f ON f.food_id = rw.food_id
                WHERE f.food_type_id = {food_type_id}"""
    db.execute(string)
    db.commit()
    return {"warehouse": True}

def delete_food(db: Session, food_type_id: int):
    num_row_deleted = db.query(models.Food).filter(models.Food.food_type_id == food_type_id).delete()
    db.commit()
    return num_row_deleted

def delete_foodtype(db: Session, food_type_id: int):
    num_row_deleted = db.query(models.FoodType).filter(models.FoodType.food_type_id == food_type_id).delete()
    db.commit()
    return num_row_deleted
