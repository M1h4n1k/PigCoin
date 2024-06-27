user_league_ranges = {
    0: (0, 499),
    1: (500, 999),
    2: (1000, None)
}

club_league_ranges = {
    0: (0, 4999),
    1: (5000, 9999),
    2: (10000, None)
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
