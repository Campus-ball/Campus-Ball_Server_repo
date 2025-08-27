from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pymongo import MongoClient
from app.core.config import settings

# SQLAlchemy (for Relational DB)
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# MongoDB (for Document DB)
mongo_client = MongoClient(settings.MONGO_DATABASE_URL)
# You can define your MongoDB database and collections here
mongo_db = mongo_client[settings.MONGO_DB_NAME]


def get_mongo_db():
    return mongo_db
