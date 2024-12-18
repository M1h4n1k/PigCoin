from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Club(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    picture: str
    tg_tag: str
    total_coins: int
    league: int
    members_count: int


class DecorationShort(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    picture: str


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserPublic(User):
    uid: str
    picture: str
    username: str
    total_coins: int
    decorations: list[DecorationShort]


class UserPrivate(UserPublic):
    tg_id: int
    current_energy: int
    max_energy: int
    turbo_available: bool

    last_ad_collected: datetime

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

    class Config:
        json_encoders = {
            datetime: lambda v: v.timestamp(),  # timezone is difficult to handle
        }


class UserCreate(User):
    tg_id: int
    picture: str
    username: str
    referrer_tg_id: int| None = None
    club_id: int| None = None


class Task(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    picture: str
    reward: int
    link: str
    type: str
    completed: bool = False


class Boost(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    picture: str
    count: int = -1
    price: int = -1


class CollectCoins(BaseModel):
    coins: int


class Transaction(BaseModel):
    model_config = ConfigDict(from_attributes=True, json_encoders={datetime: lambda v: v.timestamp()})

    amount: int
    from_user: UserPublic
    to_user: UserPublic
    created_at: datetime


class TransactionCreate(BaseModel):
    amount: int
    to_user_uid: str


class Decoration(DecorationShort):
    id: int
    title: str
    initial_price: int
    last_bet: int
    last_bet_user: UserPublic | None = None
    type: str
    betting_ends_at: datetime

    class Config:
        json_encoders = { datetime: lambda v: v.timestamp() }
