from fastapi import Request, Response, APIRouter, Depends, HTTPException, Body
from database import crud, schemas, models
from sqlalchemy.orm import Session
from dependencies import get_db, get_tg_data, get_user, validate_tg_data
import orjson

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
    user = crud.users.get_user(db, orjson.loads(tg_data)['user']['id'])
    if not user:
        tg_data_dict = orjson.loads(tg_data)
        crud.users.create_user(db, schemas.UserCreate(
            tg_id=tg_data_dict['user']['id'],
            username=tg_data_dict['user']['first_name'],
            picture='',
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
