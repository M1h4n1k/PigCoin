from .. import models, schemas
from sqlalchemy import desc, asc, func, and_
from sqlalchemy.orm import Session, query
from sqlalchemy.dialects.mysql import insert as upsert


def create_club(db: Session, club: models.Club) -> models.Club:
    db.add(club)
    db.commit()
    db.refresh(club)
    return club


def get_club(db: Session, club_id: int) -> models.Club | None:
    return db.get(models.Club, club_id)


def get_clubs_within_coins_range(db: Session, min_total_coins: int, max_total_coins: int | None, offset: int, limit: int) -> list:
    qr = db.query(models.Club).filter(models.Club.total_coins >= min_total_coins)
    if max_total_coins:
        qr = qr.filter(models.Club.total_coins <= max_total_coins)
    qr = qr.order_by(desc(models.Club.total_coins)).offset(offset).limit(limit)
    return qr.all()


# collisions are possible, research some more. Gemini suggests using sqlalchemy's versioning
def update_clubs_total_coins(db: Session, club_id: int, money: int) -> models.Club | None:
    club = db.get(models.Club, club_id)
    club.total_coins += money
    db.commit()
    db.refresh(club)
    return club


def add_member_to_club(db: Session, club_id: int) -> models.Club | None:
    club = db.get(models.Club, club_id)
    club.members_count += 1
    db.commit()
    db.refresh(club)
    return club


def remove_member_from_club(db: Session, club_id: int) -> models.Club | None:
    club = db.get(models.Club, club_id)
    club.members_count -= 1
    db.commit()
    db.refresh(club)
    return club
