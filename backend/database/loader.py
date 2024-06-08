from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os


SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://root:{os.getenv("DBPASS", "rectione")}@{os.getenv("DATABASE", "127.0.0.1")}/coin?charset=utf8mb4'


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600, pool_size=5, pool_pre_ping=True)
if not database_exists(engine.url): create_database(engine.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
