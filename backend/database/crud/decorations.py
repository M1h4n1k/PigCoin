from .. import models, schemas
from datetime import datetime
from sqlalchemy import desc, asc, and_, or_
from sqlalchemy.orm import Session, query


def get_decoration_by_id(db: Session, decoration_id: int) -> models.Decoration | None:
    return db.get(models.Decoration, decoration_id)


def make_bet(db: Session, user: models.User, decoration: models.Decoration, amount: int) -> models.Decoration:
    decoration.last_bet_user.current_coins += decoration.last_bet
    user.current_coins -= amount

    decoration.last_bet = amount
    decoration.last_bet_user = user
    db.commit()
    return decoration


def get_decoration_on_auction(db: Session) -> models.Decoration | None:
    return db.query(models.Decoration).filter(models.Decoration.betting_ends_at > datetime.now()).order_by(
        asc(models.Decoration.betting_ends_at)).first()
