from pydantic import BaseModel, Field


class Club(BaseModel):
    id: int
    name: str
    picture: str
    tg_tag: str
    total_coins: int
    league: int
    members_count: int

    class Config:
        from_attributes = True


class User(BaseModel):

    class Config:
        from_attributes = True


class UserPublic(User):
    tg_id: int
    picture: str
    username: str
    total_coins: int


class UserPrivate(UserPublic):
    tg_id: int
    current_energy: int
    max_energy: int
    turbo_available: bool

    click_price: int
    refill_rate: int
    total_coins: int
    current_coins: int
    league: int

    free_turbo: int
    free_refills: int

    club_id: int | None
    club: Club | None

    position_in_club: int | None = None
    position: int | None = None


class UserCreate(User):
    tg_id: int
    picture: str
    username: str
    referrer_tg_id: int| None = None
    club_id: int| None = None


class Task(BaseModel):
    id: int
    picture: str
    reward: int
    link: str
    type: str
    completed: bool = False

    class Config:
        from_attributes = True


class Boost(BaseModel):
    id: int
    title: str
    picture: str
    count: int = -1
    price: int = -1

    class Config:
        from_attributes = True


class CollectCoins(BaseModel):
    coins: int
