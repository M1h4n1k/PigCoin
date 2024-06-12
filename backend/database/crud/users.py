from datetime import datetime, timedelta
from .. import models, schemas
from sqlalchemy import desc, asc, func, and_
from sqlalchemy.orm import Session, query
from sqlalchemy.dialects.mysql import insert as upsert


def get_user(db: Session, user_tg_id: int) -> models.User | None:
    return db.get(models.User, user_tg_id)


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_money(db: Session, user: models.User, money: int) -> models.User:
    user.current_coins += money
    if money > 0:
        user.total_coins += money
    db.commit()
    db.refresh(user)
    return user


def update_user_turbo(db: Session, user: models.User, turbo: bool) -> models.User:
    user.turbo_available = turbo
    db.commit()
    db.refresh(user)
    return user


def user_use_free_refill(db: Session, user: models.User) -> models.User:
    user.free_refills -= 1
    user.current_energy = user.max_energy
    db.commit()
    db.refresh(user)
    return user


def user_use_free_turbo(db: Session, user: models.User) -> models.User:
    user.free_turbo -= 1
    user.turbo_available = True
    db.commit()
    db.refresh(user)
    return user


def decrease_user_energy(db: Session, user: models.User, energy: int) -> models.User:
    if energy < 0:
        raise ValueError('Energy must be positive')
    user.current_energy -= energy
    db.commit()
    db.refresh(user)
    return user


def update_user_club(db: Session, user: models.User, club_id: int) -> None:
    user.club_id = club_id
    db.commit()
    return


def update_user_picture(db: Session, user: models.User, picture: str) -> None:
    user.picture = picture
    db.commit()
    return


def get_users_within_coins_range(db: Session, min_total_coins: int, max_total_coins: int | None) -> list:
    qr = db.query(models.User).filter(models.User.total_coins >= min_total_coins)
    if max_total_coins:
        qr = qr.filter(models.User.total_coins <= max_total_coins)
    qr = qr.order_by(desc(models.User.total_coins))
    return qr.all()


def get_position_in_league(db: Session, user: models.User, coins_max: int | None) -> int:
    qr = db.query(models.User).filter(models.User.total_coins > user.total_coins)
    if coins_max:
        qr = qr.filter(models.User.total_coins <= coins_max)
    return qr.count() + 1
