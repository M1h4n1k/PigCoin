from .. import models
from datetime import datetime, timedelta
from sqlalchemy import asc
from sqlalchemy.orm import Session


def get_decoration_by_id(db: Session, decoration_id: int) -> models.Decoration | None:
    return db.get(models.Decoration, decoration_id)


def make_bet(db: Session, user: models.User, decoration: models.Decoration, amount: int) -> models.Decoration:
    if decoration.last_bet_user:
        decoration.last_bet_user.current_coins += decoration.last_bet
    user.current_coins -= amount

    decoration.last_bet = amount
    decoration.last_bet_user = user
    decoration.betting_ends_at = max(decoration.betting_ends_at, datetime.now() + timedelta(hours=1))
    db.commit()
    return decoration


def get_decoration_on_auction(db: Session) -> models.Decoration | None:
    return db.query(models.Decoration).filter(models.Decoration.betting_ends_at > datetime.now()).order_by(
        asc(models.Decoration.betting_ends_at)).first()


def finish_auction(db: Session, decoration: models.Decoration):
    decoration.last_bet_user.decorations.append(decoration)
    decoration.betting_ends_at = datetime.now()
    db.commit()
    return decoration
