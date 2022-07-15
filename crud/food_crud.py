import string
from typing import Union
from unittest import result
from sqlalchemy.orm import Session
import models
import schemas

def get_all_foods(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Food).offset(skip).limit(limit).all()

def count_all_foods_by_account(db: Session, account_id: int, query: Union[str, None] = None):
    string = f"""
    SELECT COUNT(*) AS TOTAL_ROW
    FROM restaurant_warehouse rw
    JOIN restaurant res ON res.restaurant_id = rw.restaurant_id
    JOIN seller sl ON sl.seller_id = res.seller_id
    JOIN account acc ON acc.account_id = sl.account_id
    JOIN food f ON f.food_id = rw.food_id
    WHERE (acc.account_id = {account_id}) """
    # Nếu có seach => str = Pho
    if query:
        query_str = f""" AND (f.food_name LIKE '%{query}%')"""
        string = ''.join([string, query_str])
    result = db.execute(string)
    return result.fetchall()

def get_all_foods_by_account(db: Session, account_id: int, query: Union[str, None] = None, skip: int = 0, limit: int = 100):
    string = f"""SELECT acc.account_id AS account_ID, sl.seller_id AS seller_ID, res.restaurant_id AS restaurant_ID, f.*, rw.food_quantity
FROM restaurant_warehouse rw
JOIN restaurant res ON res.restaurant_id = rw.restaurant_id
JOIN seller sl ON sl.seller_id = res.seller_id
JOIN account acc ON acc.account_id = sl.account_id
JOIN food f ON f.food_id = rw.food_id
WHERE acc.account_id = {account_id} """
    # Nếu có seach => str = Pho
    pagination = f"""LIMIT {skip}, {limit}"""
    if query:
        query_str = f"""AND (f.food_name LIKE '%{query}%') """      
        string = ''.join([string, query_str, pagination])
    else:
        string = ''.join([string, pagination])
    result = db.execute(string)
    return result.fetchall()

def get_food_from_restaurant(db: Session, restaurant_id: int, skip: int = 0, limit: int = 100):
    result = db.execute(f"""SELECT res.restaurant_id AS restaurant_ID, f.*, rw.food_quantity
FROM restaurant_warehouse rw
JOIN restaurant res ON res.restaurant_id = rw.restaurant_id
JOIN food f ON f.food_id = rw.food_id
WHERE res.restaurant_id = {restaurant_id}""")
    return result.fetchall()

def get_food_from_id(db: Session, food_id: int):
    result = db.execute(f"""SELECT f.*, rw.food_quantity
FROM food f
JOIN restaurant_warehouse rw ON rw.food_id = f.food_id
WHERE f.food_id = {food_id}""")
    return result.fetchall()

def check_duplicate_image(db: Session, image_name: str):
    count = db.query(models.Food).filter(models.Food.food_image == image_name).count()
    return count

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
    food = db.execute(f"""SELECT f.*, rw.food_quantity  , ft.food_type_name
FROM food f
JOIN restaurant_warehouse rw ON rw.food_id = f.food_id
JOIN food_type ft ON ft.food_type_id = f.food_type_id
WHERE f.food_id = {food_id}""")
    
    return food.fetchall()

def update_food_info(db: Session, food: schemas.UpdateFoodInfo, food_id: int):
    db_food = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    db_food.food_name = food.food_name
    db_food.food_price = food.food_price
    db_food.food_description = food.food_description
    db_food.food_type_id = food.food_type_id
    db.commit()
    updated_id =  db_food.food_id
    return updated_id

def update_food_image(db: Session, food: schemas.UpdateFoodImage, food_id: int):
    db_food = db.query(models.Food).filter(models.Food.food_id == food_id).first()
    db_food.food_image = food.food_image

    db.commit()
    updated_id =  db_food.food_id
    return updated_id


# Phân trang món ăn ở buyer page
def get_total_rows_food_by_restaurant_id(db: Session, restaurant_id: int, query: Union[str, None]=None):
    string = f"""SELECT COUNT(*) AS TOTAL_ROW
                FROM restaurant res
                JOIN restaurant_warehouse rw ON rw.restaurant_id = res.restaurant_id
                JOIN food f ON f.food_id = rw.food_id
                WHERE res.restaurant_id = {restaurant_id} """
    if query:
        query_str = f"""AND (f.food_name LIKE '%{query}%')"""
        string = ''.join([string, query_str])
    result = db.execute(string)
    return result.fetchall()

def get_all_rows_food_by_restaurant_id(db: Session, restaurant_id, query: Union[str, None]=None, skip: int = 0, limit: int = 10):
    string = f"""SELECT f.*, rw.food_quantity
    FROM restaurant res
    JOIN restaurant_warehouse rw ON rw.restaurant_id = res.restaurant_id
    JOIN food f ON f.food_id = rw.food_id
    WHERE (res.restaurant_id = {restaurant_id}) """

    # Nếu có seach => str = Pho
    pagination = f"""LIMIT {skip}, {limit} """
    if query:
        query_str = f"""AND (f.food_name LIKE '%{query}%') """      
        string = ''.join([string, query_str, pagination])
    else:
        string = ''.join([string, pagination])
    result = db.execute(string)
    return result.fetchall()


# API cho dashboard -----------------------------------------------------------------
def get_total_rows_food(db: Session, account_id: int):
    query = f"""SELECT COUNT(*) AS TOTAL_ROW_FOOD
                FROM account acc
                JOIN seller sl ON sl.account_id = acc.account_id
                JOIN restaurant r ON r.seller_id = sl.seller_id
                JOIN restaurant_warehouse rw ON rw.restaurant_id = r.restaurant_id
                JOIN food f ON f.food_id = rw.food_id
                WHERE (acc.account_id = {account_id}) """
    result = db.execute(query)
    return result.fetchall()

def get_list_foods_out_of_stock(db: Session, account_id: int):
    query = f"""SELECT f.food_id, f.food_name, rw.food_quantity
                FROM account acc
                JOIN seller sl ON sl.account_id = acc.account_id
                JOIN restaurant r ON r.seller_id = sl.seller_id
                JOIN restaurant_warehouse rw ON rw.restaurant_id = r.restaurant_id
                JOIN food f ON f.food_id = rw.food_id
                WHERE (acc.account_id = {account_id}) AND (rw.food_quantity = 0)"""
    result = db.execute(query)
    return result.fetchall()

# Seller delete food => not check data on order and order detail --------------------
def delete_food_in_warehouse(db: Session, food_id: int):
    num_row_deleted = db.query(models.RestaurantWarehouse).filter(models.RestaurantWarehouse.food_id == food_id).delete()
    db.commit()
    return num_row_deleted

def delete_food(db: Session, food_id: int):
    num_row_deleted = db.query(models.Food).filter(models.Food.food_id == food_id).delete()
    # if db_food is None:
    #     return {"Error": f"Food with ID {food_id} is not exists"}
    db.commit()
    return num_row_deleted



