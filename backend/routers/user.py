import logging
from aiogram import exceptions
from fastapi import Request, Response, APIRouter, Depends, HTTPException, Body
from database import crud, schemas, models
from datetime import datetime
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
        picture_path = '/pig_ava.png'
        try:
            profile_pictures = await bot.get_user_profile_photos(tg_data_dict['user']['id'], limit=1)
            if profile_pictures.total_count:
                picture_path = await load_image(profile_pictures.photos[0][0].file_id, tg_data_dict['user']['id'])
        except exceptions.TelegramBadRequest:
            logging.error(f'user not found: {tg_data_dict}')
            # raise HTTPException(status_code=404, detail='User not found')

        user = crud.users.create_user(db, schemas.UserCreate(
            tg_id=tg_data_dict['user']['id'],
            username=tg_data_dict['user']['first_name'],
            picture=picture_path,
            referrer_tg_id=start_param_data.get('userId'),
        ))
        if start_param_data.get('userId') and user.tg_id != start_param_data['userId']:
            referrer = crud.users.get_user(db, start_param_data['userId'])
            coins_gained = 25000 if tg_data_dict['user'].get('is_premium') else 5000
            crud.users.update_user_money(db, user, coins_gained)
            crud.users.update_user_money(db, referrer, coins_gained)
            if referrer.club_id:
                crud.clubs.update_clubs_total_coins(db, referrer.club_id, coins_gained)

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
    if user.club_id:
        crud.clubs.update_clubs_total_coins(db, user.club_id, user.auto_coins)
    user = crud.users.update_user_money(db, user, user.auto_coins)
    user._current_energy = user.current_energy
    user.energy_last_used = datetime.now()
    db.commit()
    db.refresh(user)
    return user
