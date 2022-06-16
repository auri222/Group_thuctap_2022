from sqlalchemy.orm import Session
from .. import models
from .. import schemas

def create_restaurant_info(db: Session, restaurant: schemas.Restaurant, seller_id: int):
    db_restaurant = models.Restaurant(  restaurant_name = restaurant.restaurant_name,
                                        restaurant_address = restaurant.restaurant_address,
                                        seller_id = seller_id)
    db.add(db_restaurant)
    db.commit()
    db.refresh(db_restaurant)
    return db_restaurant

def update_restaurant_info(db: Session, restaurant: schemas.Restaurant, seller_id: int):
    db_restaurant = db.query(models.Restaurant).filter(models.Restaurant.seller_id == seller_id).first()
    if db_restaurant is None:
        return {"Error": f"Restaurant of this Seller (ID={seller_id}) is not exits"}
    db_restaurant.restaurant_name = restaurant.restaurant_name
    db_restaurant.restaurant_address = restaurant.restaurant_address

    db.commit()
    return db_restaurant