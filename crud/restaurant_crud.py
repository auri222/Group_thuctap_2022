from msilib import schema
import string
from sqlalchemy.orm import Session
import models
import schemas

def get_all_restaurants(db: Session, skip: int =0, limit: int = 10):
    result = db.execute(f"""SELECT * FROM restaurant LIMIT {skip}, {limit} """)
    return result.fetchall()

def get_random_restaurant(db: Session, limit: int = 10):
    result = db.execute(f"""SELECT res.restaurant_id, res.restaurant_name, res.restaurant_address, res.restaurant_image
FROM restaurant res 
ORDER BY RAND()
LIMIT {limit} """)
    return result.fetchall()


def get_restaurant_info_by_ID(db: Session, restaurant_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == restaurant_id).first()

def restaurant_info_for_restaurant_index(db: Session, restaurant_id: int):
    string = f"""SELECT res.*, sl.seller_phone, sl.seller_email
FROM restaurant res
JOIN seller sl ON sl.seller_id = res.seller_id
WHERE res.restaurant_id = {restaurant_id}"""
    result = db.execute(string)
    return result.fetchall()

def get_restaurant_info_by_seller_ID(db: Session, seller_id: int):
    return db.query(models.Restaurant).filter(models.Restaurant.seller_id == seller_id).first()

def create_restaurant_info(db: Session, restaurant: schemas.CreateRestaurantInfo, seller_id: int):
    db_restaurant = models.Restaurant(  restaurant_name = restaurant.restaurant_name,
                                        restaurant_address = restaurant.restaurant_address,
                                        restaurant_image = restaurant.restaurant_image,
                                        seller_id = seller_id)
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

def update_restaurant_info(db: Session, restaurant: schemas.UpdateRestaurantInfo, restaurant_id: int):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == restaurant_id).first()
    # if db_restaurant is None:
    #     return {"Error": f"Restaurant ID {restaurant_id} is not exits"}
    db_restaurant.restaurant_name = restaurant.restaurant_name
    db_restaurant.restaurant_address = restaurant.restaurant_address

    db.commit()
    res_id = db_restaurant.restaurant_id
    return res_id

def update_restaurant_image(db: Session, restaurant: schemas.UpdateRestaurantImage, seller_id: int):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.seller_id == seller_id).first()
    if db_restaurant is None:
        return {"Error": f"Restaurant of this Seller (ID={seller_id}) is not exits"}
    db_restaurant.restaurant_image = restaurant.restaurant_image

    db.commit()
    return db_restaurant

def update_restaurant_image_by_restaurant_id(db: Session, restaurant: schemas.UpdateRestaurantImage, restaurant_id: int):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.restaurant_id == restaurant_id).first()
    # if db_restaurant is None:
    #     return {"Error": f"Restaurant of this Seller (ID={seller_id}) is not exits"}
    db_restaurant.restaurant_image = restaurant.restaurant_image

    db.commit()

    res_id = db_restaurant.restaurant_id
    return res_id

def get_list_food_type_by_restaurant_id(db: Session, restaurant_id: int):
    query = f"""SELECT ft.food_type_name
                FROM restaurant res
                JOIN restaurant_warehouse rw ON rw.restaurant_id = res.restaurant_id
                JOIN food f ON f.food_id = rw.food_id
                JOIN food_type ft ON ft.food_type_id = f.food_type_id
                WHERE res.restaurant_id = {restaurant_id}
                GROUP BY ft.food_type_id"""
    result = db.execute(query)
    return result.fetchall()

def count_all_restaurants(db: Session):
    query = f"""SELECT COUNT(*) AS TOTAL_RESTAURANT
                FROM restaurant res"""
    result = db.execute(query)
    return result.fetchall()

def fetch_row_query(db: Session, restaurant_id: int, query: str):
    string = f"""SELECT COUNT(rw.food_id) AS TOTAL_ROW
FROM restaurant res
JOIN restaurant_warehouse rw ON rw.restaurant_id = res.restaurant_id
JOIN food f ON f.food_id = rw.food_id
WHERE (res.restaurant_id = {restaurant_id}) AND (f.food_name LIKE '%{query}%')"""
    result = db.execute(string)
    return result.fetchall()