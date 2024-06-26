from fastapi import Request, Response, APIRouter, Depends, HTTPException, Body
from database import crud, schemas, models
from sqlalchemy.orm import Session
from dependencies import get_db, get_tg_data, get_user, validate_tg_data
import orjson
from utils import get_user_league_range
from bot import bot, TOKEN
import re
from hashlib import sha1
import os


router = APIRouter(prefix='/user', responses={
    400: {'description': 'No tg_data or invalid hash'},
})


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
    tg_data_dict = orjson.loads(tg_data)['user']['id']
    user = crud.users.get_user(db, tg_data_dict)
    if not user:
        profile_pictures = await bot.get_user_profile_photos(user.tg_id, limit=1)
        picture_path = '/pig_ava.png'
        if profile_pictures.total_count:
            profile_picture_file = await bot.get_file(profile_pictures.photos[0][0].file_id)
            extension = profile_picture_file.file_path.split('.')[-1]
            if re.match(r'[^a-zA-z0-9]', extension):
                raise Exception('Invalid extension')
            file_name = sha1(f'{user.tg_id}{TOKEN}'.encode()).hexdigest()
            await bot.download_file(
                profile_picture_file.file_path, os.path.join('photos', f'{file_name}.{extension}')
            )
            picture_path = f'/api/photos/{file_name}.{extension}'
        crud.users.create_user(db, schemas.UserCreate(
            tg_id=tg_data_dict['user']['id'],
            username=tg_data_dict['user']['first_name'],
            picture=picture_path,
        ))
        user = crud.users.get_user(db, tg_data_dict['user']['id'])
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
