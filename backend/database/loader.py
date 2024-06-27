from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import os
from database.models import Base, Task


SQLALCHEMY_DATABASE_URL = f'mysql+pymysql://root:{os.getenv("DBPASS", "rectione")}@{os.getenv("DATABASE", "127.0.0.1")}/coin?charset=utf8mb4'


engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_recycle=3600, pool_size=5, pool_pre_ping=True)
if not database_exists(engine.url): create_database(engine.url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@event.listens_for(Base.metadata, 'after_create')
def create_initialize_tasks(*args, **kw):
    db = SessionLocal()
    if db.query(Task).count() > 0:
        db.close()
        return
    db.add_all([
        Task(
            id=1,
            title='Join the channel',
            picture='/telegram.svg',
            reward=120,
            link='https://t.me/M1h4n1k_sub_task1',
            type='subscribe'
        ),
        Task(
            id=2,
            title='Join the channel',
            picture='/telegram.svg',
            reward=120,
            link='https://t.me/M1h4n1k_sub_task2',
            type='subscribe'
        ),
        Task(
            id=3,
            title='Invite a fren',
            picture='/addFren.svg',
            reward=240,
            link='',
            type='invite'
        ),
    ])
    db.commit()
    db.close()


Base.metadata.create_all(bind=engine)
