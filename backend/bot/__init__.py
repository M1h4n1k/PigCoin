from .middlewares import on_pre_process
from .handlers import *
from .loader import dp, TOKEN, bot


def register_handlers():
    dp.message.middleware(on_pre_process)
    dp.message.register(default_handler)


register_handlers()

__all__ = ['TOKEN', 'dp', 'bot']
