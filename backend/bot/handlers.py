from aiogram import types, exceptions
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import (
    InlineKeyboardButton,
    Message
)
import urllib.parse
from utils import get_locale as __
from .loader import WEB_LINK, bot


async def default_handler(message: Message):
    # res = await bot.get_user_profile_photos(message.from_user.id, limit=1)
    # ff = await bot.get_file(res.photos[0][0].file_id)
    # print(bot.download_file())
    if message.text is None:
        return await message.answer(__('start', message.from_user.language_code))
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
        text=__('open', message.from_user.language_code) + WEB_LINK,
        web_app=WebAppInfo(url=WEB_LINK))
    ]])
    await message.answer(
        __("start", message.from_user.language_code),
        reply_markup=kb, parse_mode='HTML'
    )
