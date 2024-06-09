from pydantic import BaseModel


class User(BaseModel):

    class Config:
        from_attributes = True


class UserPublic(User):
    picture: str
    username: str
    total_coins: int
    league: int


class UserPrivate(UserPublic):
    tg_id: int
    current_energy: int
    max_energy: int
    turbo_available: bool

    total_coins: int
    current_coins: int

    free_turbo: int
    free_refills: int

    club_id: int | None
    club: dict | None


class UserCreate(User):
    picture: str
    username: str
    referrer_tg_id: int| None = None
    club_id: int| None = None


class Task(BaseModel):
    id: int
    title: str
    picture: str
    reward: int
    link: str
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


class Club(BaseModel):
    id: int
    name: str
    picture: str
    tg_link: str
    total_coins: int
    league: int

    class Config:
        from_attributes = True
