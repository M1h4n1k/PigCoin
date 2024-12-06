import os
from aiogram import Bot, Dispatcher

TOKEN = os.environ.get('BOT_TOKEN') or 'from @BotFather'
WEB_LINK = os.environ.get('WEB_LINK') or 'http://127.0.0.1:3000'
ADMINS = [1044949157, 5000204712]

bot = Bot(token=TOKEN)
dp = Dispatcher()

