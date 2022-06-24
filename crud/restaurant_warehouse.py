from sqlalchemy.orm import Session
import models
import schemas

def create_restaurant_warehouse_info(db: Session, restaurant_warehouse: schemas.RestaurantWarehouse):
    db_restaurant_warehouse = models.RestaurantWarehouse(restaurant_id = restaurant_warehouse.restaurant_id,
                                                        food_id = restaurant_warehouse.food_id,
                                                        food_quantity = restaurant_warehouse.food_quantity)
    db.add(db_restaurant_warehouse)
    db.commit()
    db.refresh(db_restaurant_warehouse)
    return db_restaurant_warehouse

def get_restaurant_warehouse_info_by_restaurant_id(db: Session, restaurant_id: int):
    return db.query(models.RestaurantWarehouse).filter(models.RestaurantWarehouse.restaurant_id == restaurant_id).first()

