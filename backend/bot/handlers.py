from aiogram import types, exceptions
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import (
    InlineKeyboardButton,
    Message,
    ChatMemberUpdated
)
from utils import get_locale as __, load_image
from .loader import WEB_LINK, bot
from database.loader import SessionLocal
from database import crud, schemas


async def default_handler(message: Message):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text=__('open', message.from_user.language_code),
        web_app=WebAppInfo(url=WEB_LINK))
    ]])
    await message.answer(
        __("start", message.from_user.language_code),
        reply_markup=kb, parse_mode='HTML'
    )


async def on_user_join(event: ChatMemberUpdated):
    channel_tasks = {
        'M1h4n1k_sub_task1': 1,
    }
    db = SessionLocal()
    user = crud.users.get_user(db, event.from_user.id)
    # TODO referrer will be empty in this case and it will not be possible to set it again,
    #  but if a user has already found the channel himself then probably he will not need a referrer
    if user is None:
        profile_pictures = await bot.get_user_profile_photos(event.from_user.id, limit=1)
        picture_path = '/pig_ava.png'
        if profile_pictures.total_count:
            picture_path = await load_image(profile_pictures.photos[0][0].file_id, event.from_user.id)

        crud.users.create_user(db, schemas.UserCreate(
            tg_id=event.from_user.id,
            username=event.from_user.first_name,
            picture=picture_path,
        ))
        user = crud.users.get_user(db, event.from_user.id)
    if any(task.id == channel_tasks[event.chat.username] for task in user.tasks_completed):
        db.close()
        return
    crud.tasks.complete_task(db, channel_tasks[event.chat.username], event.from_user.id)
    db.close()
    return
