import os
from aiogram import Bot, Dispatcher

TOKEN = os.environ.get('BOT_TOKEN') or '5000485989:AAHhaZ_4NXppwOULMmY81rIJoder_CKlbwI/test'
WEB_LINK = os.environ.get('WEB_LINK') or 'http://127.0.0.1:3000'  # 'http://84.249.33.163:8080/'
ADMINS = [1044949157, 5000204712]

bot = Bot(token=TOKEN)
dp = Dispatcher()

