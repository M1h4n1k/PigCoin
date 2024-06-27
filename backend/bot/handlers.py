from aiogram import types, exceptions
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import (
    InlineKeyboardButton,
    Message,
    ChatMemberUpdated
)
from utils import get_locale as __
from .loader import WEB_LINK
from database.loader import SessionLocal
from database import crud


async def default_handler(message: Message):
    if message.text is None:
        return await message.answer(__('start', message.from_user.language_code))
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
    # TODO probably it's possible that a user can join the channel without starting the bot
    if user is None:
        raise Exception('on_user_join (0): Not yet implemented')
    if any(task.id == channel_tasks[event.chat.username] for task in user.tasks_completed):
        db.close()
        return
    crud.tasks.complete_task(db, channel_tasks[event.chat.username], event.from_user.id)
    db.close()
    return
