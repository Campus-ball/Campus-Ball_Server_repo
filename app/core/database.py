from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pymongo import MongoClient
from app.core.settings import get_settings

# SQLAlchemy (for Relational DB)
settings = get_settings()
engine = create_engine(
    settings.resolved_database_url,
    pool_pre_ping=True,
    future=True,
    echo=settings.sqlalchemy_echo,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# MongoDB (for Document DB)
if settings.mongo_database_url:
    mongo_client = MongoClient(settings.mongo_database_url)
    mongo_db = mongo_client[settings.mongo_db_name] if settings.mongo_db_name else None
else:
    mongo_client = None
    mongo_db = None
# You can define your MongoDB database and collections here
mongo_db = mongo_client[settings.MONGO_DB_NAME]


def get_mongo_db():
    return mongo_db
