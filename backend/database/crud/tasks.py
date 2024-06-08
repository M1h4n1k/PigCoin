from datetime import datetime, timedelta

from .. import models, schemas
from sqlalchemy import desc, asc, func, and_
from sqlalchemy.orm import Session, query


def get_tasks(db: Session) -> list:
    return db.query(models.Task).all()


def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def complete_task(db: Session, task_id: int, user_tg_id: int) -> None:
    db.add(models.UserTask(user_tg_id=user_tg_id, task_id=task_id))
    db.commit()
    return

