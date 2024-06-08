from fastapi import Request, Response, APIRouter, Depends, HTTPException
from database import crud, schemas, models
from sqlalchemy.orm import Session
from dependencies import get_db, get_tg_data, get_user_optional, get_user
import orjson

router = APIRouter(prefix='/user', responses={
    400: {'description': 'No tg_data or invalid hash'},
})


@router.post(
    '/login',
    response_model=str,
    status_code=200,
)
async def login(
    response: Response,
    tg_data: dict = Depends(get_tg_data),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user_optional)
):
    response.set_cookie(key='tg_data', value=orjson.dumps(tg_data).decode(), httponly=True)
    print(tg_data)
    if not user:
        crud.users.create_user(db, schemas.UserCreate(**tg_data))
    return 'OK'


@router.get(
    '/data',
    response_model=schemas.UserPrivate,
    status_code=200,
    responses={
        404: {'description': 'User not found'},
    }
)
async def get_user_data(user: models.User = Depends(get_user)):
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
