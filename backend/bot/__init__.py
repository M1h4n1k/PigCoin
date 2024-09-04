from .middlewares import create_user
from .handlers import *
from .loader import dp, TOKEN, bot
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
# from aiogram import types


def register_handlers(_dp):
    _dp.message.middleware(create_user)
    _dp.message.register(default_handler)
    _dp.chat_member.register(on_user_join, ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))


register_handlers(dp)

__all__ = ['TOKEN', 'dp', 'bot', 'register_handlers']
