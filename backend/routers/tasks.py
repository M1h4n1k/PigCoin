from fastapi import Request, Response, APIRouter, Depends, HTTPException
from database import crud, schemas, models
from sqlalchemy.orm import Session
from dependencies import get_db, get_user
import orjson
from bot import bot


router = APIRouter(prefix='/tasks', responses={404: {'description': 'User not found'}})


@router.get(
    '/',
    response_model=list[schemas.Task],
    status_code=200,
)
async def all_tasks(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user)
) -> list[schemas.Task]:
    tasks = crud.tasks.get_tasks(db)  # small, less than 10-20
    for tc in tasks:  # <= len(tasks)
        if any(tc.id == task.id for task in user.tasks_completed):
            tc.completed = True
    return tasks


@router.post(
    '/{task_id}/complete',
    status_code=200,
    responses={
        400: {'description': 'Task already completed'},
        404: {'description': 'Task or user not found'},
    },
)
async def complete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user)
) -> Response:
    task = crud.tasks.get_task(db, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    if any(tc.id == task_id for tc in user.tasks_completed):
        raise HTTPException(status_code=400, detail='Task already completed')
    crud.users.update_user_money(db, user, task.reward)
    crud.clubs.update_clubs_total_coins(db, user.club_id, task.reward)
    crud.tasks.complete_task(db, task_id, user.tg_id)
    return Response(status_code=200)

