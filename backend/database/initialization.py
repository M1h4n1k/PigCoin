from database.models import Base, Task, Boost
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
        Task(
            id=4,
            title='Check the music bot',
            picture='/bot.svg',
            reward=240,
            link='https://t.me/M1h4n1kStageBot',
            type='bot'
        ),
    ])


def create_boosts(db):
    db.add_all([
        Boost(
            id=1,
            title='Sponge',
            picture='/sponge.png',
            base_price=10,
            coins=10,
            type='click_price'
        ),
        Boost(
            id=2,
            title='Bottle capacity',
            picture='/bottle.png',
            base_price=10,
            coins=10,
            type='capacity'
        ),
        Boost(
            id=3,
            title='Refill rate',
            picture='/refill.png',
            base_price=10,
            coins=10,
            type='refill_rate'
        ),
        Boost(
            id=4,
            title='Herdsman',
            picture='/farmer.png',
            base_price=100,
            coins=100,
            type='auto'
        ),
    ])


@event.listens_for(Base.metadata, 'after_create')
def create_initialize_database(*args, **kw):
    db = SessionLocal()
    if db.query(Task).count() == 0:
        create_tasks(db)

    if db.query(Boost).count() == 0:
        create_boosts(db)

    db.commit()
    db.close()


def init():
    Base.metadata.create_all(bind=engine)
