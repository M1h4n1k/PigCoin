from database import crud, schemas
from database.loader import SessionLocal
from datetime import datetime


async def on_pre_process(hdlr, message, data):
    data['db'] = SessionLocal()
    if message and crud.users.get_user(data['db'], message.from_user.id) is None:
        user_create = schemas.UserCreate(
            tg_id=message.from_user.id,
            username=message.from_user.username,
            picture='',
        )
        crud.users.create_user(data['db'], user_create)
    resp = await hdlr(message, data)
    data['db'].close()
    return resp
