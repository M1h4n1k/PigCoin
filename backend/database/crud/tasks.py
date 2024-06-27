from datetime import datetime, timedelta
from .. import models, schemas
from .users import update_user_money
from sqlalchemy import desc, asc, func, and_
from sqlalchemy.orm import Session, query


def get_tasks(db: Session) -> list:
    return db.query(models.Task).all()


def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.get(models.Task, task_id)


def complete_task(db: Session, task_id: int, user_tg_id: int) -> None:
    task = db.get(models.Task, task_id)
    user = db.get(models.User, user_tg_id)
    if user is None or task is None:
        raise ValueError('User or Task not found')
    update_user_money(db, user, task.reward)
    db.add(models.UserTask(user_tg_id=user_tg_id, task_id=task_id))
    db.commit()
    return

