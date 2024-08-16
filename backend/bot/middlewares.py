from database import crud, schemas
from database.loader import SessionLocal
from utils import load_image
from .loader import bot


async def create_user(hdlr, message, data):
    data['db'] = SessionLocal()
    if message and message.text and crud.users.get_user(data['db'], message.from_user.id) is None:
        # TODO test
        profile_pictures = await bot.get_user_profile_photos(message.from_user.id, limit=1)
        picture_path = '/pig_ava.png'
        if profile_pictures.total_count:
            picture_path = await load_image(profile_pictures.photos[0][0].file_id, message.from_user.id)

        user_create = schemas.UserCreate(
            tg_id=message.from_user.id,
            username=message.from_user.username,
            picture=picture_path,
        )
        crud.users.create_user(data['db'], user_create)
    resp = await hdlr(message, data)
    data['db'].close()
    return resp
