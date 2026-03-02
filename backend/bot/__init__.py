from .middlewares import create_user
from .handlers import on_user_join, default_handler
from .admin import setup_spam_message, send_spam_message
from .loader import dp, TOKEN, bot
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter, Command


def register_handlers(_dp):
    _dp.message.register(setup_spam_message, Command("spam"))
    _dp.callback_query.register(send_spam_message, lambda c: c.data == "accept_spam")

    _dp.message.middleware(create_user)
    _dp.message.register(default_handler)
    _dp.chat_member.register(
        on_user_join, ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER)
    )


register_handlers(dp)

__all__ = ["TOKEN", "dp", "bot", "register_handlers", "WEB_LINK"]
