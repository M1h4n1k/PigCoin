from datetime import datetime, timedelta
from .. import models, schemas
from sqlalchemy import desc, asc, func, and_
from sqlalchemy.orm import Session, query


def get_boost(db: Session, boost_id) -> models.Boost | None:
    return db.get(models.Boost, boost_id)


def get_boosts(db: Session) -> list[models.Boost]:
    return db.query(models.Boost).all()


def buy_boost(db: Session, user_tg_id: int, boost_id: int, boost_type: str) -> None:
    user_boost = db.query(models.UserBoost).filter(and_(
        models.UserBoost.user_tg_id == user_tg_id,
        models.UserBoost.boost_id == boost_id
    )).first()
    if user_boost:
        user_boost.count += 1
    else:
        db.add(models.UserBoost(user_tg_id=user_tg_id, boost_id=boost_id, boost_type=boost_type, count=1))
    db.commit()
    return



