from .middlewares import create_user
from .handlers import *
from .admin import *
from .loader import dp, TOKEN, bot
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, Command
# from aiogram import types


def register_handlers(_dp):
    _dp.message(Command('spam'))(setup_spam_message)
    _dp.callback_query(lambda c: c.data == 'accept_spam')(send_spam_message)

    _dp.message.middleware(create_user)
    _dp.message.register(default_handler)
    _dp.chat_member.register(on_user_join, ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))



register_handlers(dp)

__all__ = ['TOKEN', 'dp', 'bot', 'register_handlers', 'WEB_LINK']
