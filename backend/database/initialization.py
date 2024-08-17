import os
from database.models import Base, Task, Boost
from sqlalchemy import event
from database.loader import engine, SessionLocal


def create_tasks(db):
    tasks = []
    for channel in os.getenv('PROMO_CHANNELS').split(','):
        tasks.append(Task(
            id=len(tasks) + 1,
            title='Join the channel',
            picture='/telegram.svg',
            reward=500,
            link='https://t.me/' + channel,
            type='subscribe'
        ))

    tasks.append(Task(
        id=len(tasks) + 1,
        title='Invite a fren',
        picture='/addFren.svg',
        reward=1000,
        link='',
        type='invite'
    ))

    for bot in os.getenv('PROMO_BOTS').split(','):
        tasks.append(Task(
            id=len(tasks) + 1,
            title='Open bot',
            picture='/bot.svg',
            reward=1500,
            link='https://t.me/' + bot,
            type='bot'
        ))

    db.add_all(tasks)


def create_boosts(db):
    db.add_all([
        Boost(
            id=1,
            title='Sponge',
            picture='/sponge.png',
            base_price=100,
            coins=100,
            type='click_price'
        ),
        Boost(
            id=2,
            title='Bottle capacity',
            picture='/bottle.png',
            base_price=100,
            coins=100,
            type='capacity'
        ),
        Boost(
            id=3,
            title='Refill rate',
            picture='/refill.png',
            base_price=100,
            coins=100,
            type='refill_rate'
        ),
        Boost(
            id=4,
            title='Herdsman',
            picture='/farmer.png',
            base_price=1000,
            coins=1000,
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
