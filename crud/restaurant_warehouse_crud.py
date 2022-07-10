from sqlalchemy.orm import Session
import models
import schemas

def create_restaurant_warehouse_info(db: Session, restaurant_warehouse: schemas.CreateRestaurantWarehouse, restaurant_id: int, food_id: int):
    db_restaurant_warehouse = models.RestaurantWarehouse(restaurant_id = restaurant_id,
                                                        food_id = food_id,
                                                        food_quantity = restaurant_warehouse.food_quantity)
    db.add(db_restaurant_warehouse)
    db.commit()
    db.refresh(db_restaurant_warehouse)
    return db_restaurant_warehouse

def get_restaurant_warehouse_info_by_restaurant_id(db: Session, restaurant_id: int):
    return db.query(models.RestaurantWarehouse).filter(models.RestaurantWarehouse.restaurant_id == restaurant_id).first()

def update_food_quantity_by_food_id(db: Session, restaurant_warehouse: schemas.UpdateRestaurantWarehouse, food_id: int):
    db_warehouse = db.query(models.RestaurantWarehouse).filter(models.RestaurantWarehouse.food_id == food_id).first()
    db_warehouse.food_quantity = restaurant_warehouse.food_quantity
    db.commit()
    quantity = db_warehouse.food_quantity
    return quantity
