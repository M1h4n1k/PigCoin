from database.models import Base, Task
from sqlalchemy import event
from database.loader import engine, SessionLocal


def create_tasks(db):
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


@event.listens_for(Base.metadata, 'after_create')
def create_initialize_tasks(*args, **kw):
    db = SessionLocal()
    if db.query(Task).count() == 0:
        create_tasks(db)

    db.commit()
    db.close()


def init():
    Base.metadata.create_all(bind=engine)
