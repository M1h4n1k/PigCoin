from .. import models, schemas
from datetime import datetime
from sqlalchemy import desc, asc, and_, or_
from sqlalchemy.orm import Session, query


def get_user_by_uid(db: Session, uid: int) -> models.User | None:
    return db.query(models.User).filter(
        or_(
            and_(
                uid == models.User.tg_id * 791 - (models.User.referrer_tg_id * 10),
                models.User.referrer_tg_id.isnot(None)
            ),
            uid == models.User.tg_id * 791 - (391016011758 * 10),
        )
    ).first()


def get_user(db: Session, user_tg_id: int) -> models.User | None:
    return db.get(models.User, user_tg_id)


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_money(db: Session, user: models.User, money: int) -> models.User:
    user.current_coins += money
    if money > 0:
        user.total_coins += money
    user.last_coin_collected = datetime.now()
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


def update_user_club(db: Session, user: models.User, club_id: int | None) -> None:
    from . import clubs
    if user.club_id:
        clubs.remove_member_from_club(db, user.club_id)
    user.club_id = club_id
    if club_id:
        clubs.add_member_to_club(db, club_id)
    db.commit()
    return


def update_user_picture(db: Session, user: models.User, picture: str) -> None:
    user.picture = picture
    db.commit()
    return


def get_users_within_coins_range(db: Session, min_total_coins: int, max_total_coins: int | None, offset: int, limit: int) -> list:
    qr = db.query(models.User).filter(models.User.total_coins >= min_total_coins)
    if max_total_coins:
        qr = qr.filter(models.User.total_coins <= max_total_coins)
    qr = qr.order_by(desc(models.User.total_coins)).offset(offset).limit(limit)
    return qr.all()


def get_position_in_league(db: Session, user: models.User, coins_max: int | None) -> int:
    qr = db.query(models.User).filter(models.User.total_coins > user.total_coins)
    if coins_max:
        qr = qr.filter(models.User.total_coins <= coins_max)
    return qr.count() + 1


def update_cheated_count(db: Session, user: models.User, count: int) -> models.User:
    user.cheated_count += count
    db.commit()
    db.refresh(user)
    return user


def make_transaction(db: Session, from_user: models.User, to_user: models.User, amount: int) -> models.Transaction:
    transaction = models.Transaction(
        from_user_id=from_user.tg_id,
        to_user_id=to_user.tg_id,
        amount=amount,
        created_at=datetime.now()
    )
    db.add(transaction)
    from_user.current_coins -= amount
    to_user.current_coins += amount
    db.commit()
    db.refresh(transaction)
    return transaction


def get_transactions(db: Session, user: models.User, offset: int, limit: int) -> list[type[models.Transaction]]:
    return db.query(models.Transaction).filter(
        or_(
            models.Transaction.from_user_id == user.tg_id,
            models.Transaction.to_user_id == user.tg_id
        )
    ).order_by(desc(models.Transaction.created_at)).offset(offset).limit(limit).all()
