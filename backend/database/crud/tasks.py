from datetime import datetime, timedelta
from .. import models, schemas
from .users import update_user_money
from .clubs import update_clubs_total_coins
from sqlalchemy import desc, asc, func, and_
from sqlalchemy.orm import Session, query
from math import floor


def get_tasks(db: Session) -> list:
    return db.query(models.Task).all()


def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.get(models.Task, task_id)


def complete_task(db: Session, task_id: int, user_tg_id: int) -> None:
    task = db.get(models.Task, task_id)
    if task is None:
        raise ValueError('Task not found')
    user = db.get(models.User, user_tg_id)
    if user is None:
        raise ValueError('User not found')
    update_user_money(db, user, task.reward)
    if user.club_id:
        update_clubs_total_coins(db, user.club_id, task.reward)
    db.add(models.UserTask(user_tg_id=user_tg_id, task_id=task_id))
    db.commit()
    return


def watch_ad(db: Session, user_tg_id: int):
    user = db.get(models.User, user_tg_id)
    if user is None:
        raise ValueError('User not found')
    if not user.can_collect_ad:
        raise ValueError('You can watch ads only once in 1.2 hours')
    update_user_money(db, user, floor(user.total_coins * 0.03))
    if user.club_id:
        update_clubs_total_coins(db, user.club_id, 500)
    user.last_ad_collected = datetime.now()
    db.commit()
    db.refresh(user)
    return user

