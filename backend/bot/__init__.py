from .middlewares import on_pre_process
from .handlers import *
from .loader import dp, TOKEN, bot
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
# from aiogram import types


def register_handlers():
    dp.message.middleware(on_pre_process)
    dp.message.register(default_handler)
    dp.chat_member.register(on_user_join, ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))


register_handlers()

__all__ = ['TOKEN', 'dp', 'bot']
