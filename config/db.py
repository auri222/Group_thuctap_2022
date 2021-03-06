from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root@localhost:3306/food_delivery"

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=30, max_overflow=120)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_database_session():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()