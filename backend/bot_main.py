from bot import dp, bot
import logging

logging.basicConfig(level=logging.INFO)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
