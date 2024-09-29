from sqlalchemy import and_
from bot import WEB_LINK, bot
from database import crud, models
from datetime import datetime, timedelta
from aiogram import types, exceptions
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import InlineKeyboardButton
from utils import get_locale as __
from database.loader import SessionLocal
import asyncio


kb = types.InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(
    text=__('open', 'ru'),
    web_app=WebAppInfo(url=WEB_LINK))
]])


async def notify_auto_coins():
    db = SessionLocal()

    users = db.query(models.User).filter(
        and_(
            models.User.energy_last_used <= datetime.now() - timedelta(hours=5),
            models.User.energy_last_used > datetime.now() - timedelta(hours=6)
        )
    ).all()

    def get_ending(n: int) -> str:
        if n % 10 == 1 and n % 100 != 11:
            return ''
        elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
            return 'а'
        else:
            return 'ов'
    ge = get_ending
    for user in users:
        try:
            await bot.send_message(
                user.tg_id,
                f'За время отсутствия свинопас отмыл {user.auto_coins} ХрюКоин{ge(user.auto_coins)}!',
                reply_markup=kb
            )
        except Exception as e:
            pass

    db.close()
    return


if __name__ == '__main__':
    asyncio.run(notify_auto_coins())

