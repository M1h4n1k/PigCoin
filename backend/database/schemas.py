from pydantic import BaseModel


class User(BaseModel):
    tg_id: int

    class Config:
        from_attributes = True


class UserPublic(User):
    picture: str
    username: str
    league: int


class UserPrivate(UserPublic):
    referrer_tg_id: int
    club_id: int

    current_energy: int
    turbo_available: bool

    total_coins: int
    current_coins: int

    free_turbo: int
    free_refills: int

    club: dict


class UserCreate(User):
    picture: str
    username: str
    referrer_tg_id: int = None
    club_id: int = None

    @classmethod
    def from_tg_data(cls, tg_data: dict) -> "UserCreate":
        return cls(**tg_data)


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
    bonus: int
    count: int
    price: int

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
