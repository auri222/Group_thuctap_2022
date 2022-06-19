from sqlalchemy.orm import Session
import models
import schemas

def get_admin_by_ID(db: Session, admin_id: int):
    return db.query(models.Admin).filter(models.Admin.admin_id == admin_id).first()

def get_admin_by_email(db: Session, email: str):
    return db.query(models.Admin).filter(models.Admin.admin_email == email).first()

def get_all_admins(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Admin).offset(skip).limit(limit).all()

def create_admin_info(db: Session, admin: schemas.CreateAdminInfo, account_id: int):
    db_user = models.Admin( admin_name=admin.admin_name, 
                            admin_birthday=admin.admin_birthday, 
                            admin_address=admin.admin_address, 
                            admin_phone=admin.admin_phone, 
                            admin_email= admin.admin_email,
                            account_id=account_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_admin_return_ID(db: Session, admin: schemas.Admin, account_id: int):
    db_admin = models.Admin(admin_name=admin.admin_name, 
                                admin_birthday=admin.admin_birthday, 
                                admin_address=admin.admin_address, 
                                admin_phone=admin.admin_phone, 
                                admin_email= admin.admin_email,
                                account_id=account_id)
    db.add(db_admin)
    db.commit()
    admin_id = db_admin.admin_id
    db.refresh(db_admin)
    return admin_id


def update_admin(db: Session, admin: schemas.Admin, admin_id: int):
    db_admin = db.query(models.Admin).filter(models.Admin.admin_id == admin_id).first()
    if db_admin is None:
        return {"Error": None}
    db_admin.admin_name = admin.admin_name
    db_admin.admin_birthday = admin.admin_birthday
    db_admin.admin_address = admin.admin_address
    db_admin.admin_phone = admin.admin_phone
    db_admin.admin_email = admin.admin_email
    # db.add(db_user)
    db.commit()
    # db.refresh(db_user)
    return db_admin

def delete_admin(db: Session, admin_id: int):
    db_admin = db.query(models.Admin).filter(models.Admin.admin_id == admin_id).first()
    if db_admin is None:
        return False
    db.delete(db_admin)
    db.commit()
    return True

# def create_food_info(db: Session, food_info: admin_schema.Food, owner_id: int):
#     db_food = admin_model.Food(food_name = food_info.food_name, 
#                             food_description = food_info.food_description,
#                             food_image = food_info.food_image,
#                             owner_id = owner_id)
#     db.add(db_food)
#     db.commit()
#     db.refresh(db_food)
#     return db_food

# def update_food_image(db: Session, food_id: int, food_name: str):
#     db_food = db.query(admin_model.Food).filter(admin_model.Food.food_id == food_id).first()
#     if db_food is None:
#         return {"Error": f"Food with id {food_id} is not exists"}
#     db_food.food_image = food_name
#     # db.add(db_food)
#     db.commit()
#     return db_food
    

