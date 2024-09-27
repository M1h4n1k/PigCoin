from aiogram.types import File
from hashlib import sha1
import re
import os


user_league_ranges = {
    0: (0, 99_999),
    1: (100_000, 499_999),
    2: (500_000, 2_000_000),
    3: (2_000_000, None)
}

club_league_ranges = {
    0: (0, 99_999),
    1: (100_000, 699_999),
    2: (700_000, 1_999_999),
    3: (2_000_000, None)
}


def get_user_league(total_coins: int) -> int:
    for league, (min_coins, max_coins) in user_league_ranges.items():
        if min_coins <= total_coins < (max_coins if max_coins else total_coins + 1):
            return league


def get_club_league(total_coins: int) -> int:
    for league, (min_coins, max_coins) in club_league_ranges.items():
        if min_coins <= total_coins < (max_coins if max_coins else total_coins + 1):
            return league


def get_user_league_range(legion: int) -> tuple[int, int | None]:
    return user_league_ranges[legion]


def get_club_league_range(legion: int) -> tuple[int, int | None]:
    return club_league_ranges[legion]


def get_locale(msg: str, lang: str) -> str:
    locales = {
        'en': {
            'start': 'Start playing',
            'open': 'Open',
        },
        'ru': {
            'start': 'Начать играть',
            'open': 'Открыть',
        }
    }
    return locales.get(lang, locales['en']).get(msg)


async def load_image(file_id: str, owner_id: int) -> str:
    from bot import bot, TOKEN  # otherwise circular import

    picture_file = await bot.get_file(file_id)
    extension = picture_file.file_path.split('.')[-1]
    if re.match(r'[^a-zA-z0-9]', extension):
        raise Exception('Invalid extension')
    file_name = sha1(f'{owner_id}{TOKEN}'.encode()).hexdigest()
    await bot.download_file(
        picture_file.file_path, os.path.join('photos', f'{file_name}.{extension}')
    )
    return f'/api/photos/{file_name}.{extension}'
