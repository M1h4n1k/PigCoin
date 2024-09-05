from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os


SQLALCHEMY_DATABASE_URL = (f'mysql+pymysql://'
                           f'root:{os.getenv("MYSQL_PASSWORD", "rectione")}@{os.getenv("MYSQL_HOST", "127.0.0.1")}/'
                           f'{os.getenv("MYSQL_DATABASE", "coin")}?charset=utf8mb4')


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600, pool_size=5, max_overflow=10, pool_pre_ping=True)
if not database_exists(engine.url):
    create_database(engine.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

