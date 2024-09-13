import logging
from aiogram import exceptions
from fastapi import Request, Response, APIRouter, Depends, HTTPException, Body
from database import crud, schemas, models
from sqlalchemy.orm import Session
from dependencies import get_db, get_tg_data, get_user, validate_tg_data
import orjson
from utils import get_user_league_range, load_image
from bot import bot
import re


router = APIRouter(prefix='/user', responses={
    400: {'description': 'No tg_data or invalid hash'},
})


def parse_start_param(start_param: str | None) -> dict:
    if start_param is None:
        return {}
    if not re.match(r'^[\da-f]+(_[\da-f]+)?$', start_param):
        raise HTTPException(status_code=400, detail='Invalid start_param')
    start_param_split = start_param.split('_')
    return {
        'userId': int(start_param_split[0], 16),
        'clubId': int(start_param_split[1], 16) * -1 if len(start_param_split) > 1 else None,
    }


@router.post(
    '/login',
    response_model=schemas.UserPrivate,
    status_code=200,
)
async def login(
    response: Response,
    tg_data: str = Body(...),
    db: Session = Depends(get_db),
):
    if not validate_tg_data(tg_data):
        raise HTTPException(status_code=403, detail='Invalid hash')
    response.set_cookie(key='tg_data', value=tg_data, httponly=True)
    tg_data_dict = orjson.loads(tg_data)
    user = crud.users.get_user(db, tg_data_dict['user']['id'])
    start_param_data = parse_start_param(tg_data_dict.get('start_param'))

    if not user:
        try:
            profile_pictures = await bot.get_user_profile_photos(tg_data_dict['user']['id'], limit=1)
        except exceptions.TelegramBadRequest:
            logging.error(f'user not found: {tg_data_dict}')
            return HTTPException(status_code=404, detail='User not found')
        picture_path = '/pig_ava.png'
        if profile_pictures.total_count:
            picture_path = await load_image(profile_pictures.photos[0][0].file_id, tg_data_dict['user']['id'])

        user = crud.users.create_user(db, schemas.UserCreate(
            tg_id=tg_data_dict['user']['id'],
            username=tg_data_dict['user']['first_name'],
            picture=picture_path,
            referrer_tg_id=start_param_data.get('userId'),
        ))
        if start_param_data.get('userId') and user.tg_id != start_param_data['userId']:
            referrer = crud.users.get_user(db, start_param_data['userId'])
            crud.users.update_user_money(db, user, 25000 if tg_data_dict['user'].get('is_premium') else 5000)
            crud.users.update_user_money(db, referrer, 25000 if tg_data_dict['user'].get('is_premium') else 5000)
            tasks = crud.tasks.get_tasks(db)
            task_id = next(filter(lambda x: x.type == 'invite', tasks)).id
            if not any(task.id == task_id for task in referrer.tasks_completed):
                crud.tasks.complete_task(db, task_id, referrer.tg_id)

    if start_param_data.get('clubId'):
        crud.users.update_user_club(db, user, start_param_data['clubId'])

    return user


@router.get(
    '/referrals',
    response_model=list[schemas.UserPublic],
    status_code=200,
    responses={
        404: {'description': 'User not found'},
    }
)
async def get_referrals(user: models.User = Depends(get_user)):
    return user.referrals


@router.get(
    '/position',
    response_model=int,
    status_code=200,
    responses={
        404: {'description': 'User not found'},
    }
)
async def get_position(db: Session = Depends(get_db), user: models.User = Depends(get_user)):
    return crud.users.get_position_in_league(db, user, get_user_league_range(user.league)[1])


@router.get(
    '/autoCoins',
    response_model=int,
    status_code=200,
)
async def collect_auto_coins(
    user: models.User = Depends(get_user),
):
    return user.auto_coins


@router.post(
    '/autoCoins',
    response_model=schemas.UserPrivate,
    status_code=200,
)
async def collect_auto_coins(
    user: models.User = Depends(get_user),
    db: Session = Depends(get_db),
):
    user = crud.users.update_user_money(db, user, user.auto_coins)
    return user
