from typing import Annotated

from fastapi import Request, APIRouter, Depends, HTTPException, Body, Form
from database import crud, schemas, models
from sqlalchemy.orm import Session
from dependencies import get_db, get_user


router = APIRouter(prefix='/game', responses={404: {'description': 'User not found'}})


@router.post(
    '/collectCoins',
    response_model=schemas.UserPrivate,
    status_code=200,
    responses={
        400: {'description': 'Coins should be positive or Not enough energy'},
    },
)
async def collect_coin(
    coins: schemas.CollectCoins,
    user: models.User = Depends(get_user),
    db: Session = Depends(get_db),
) -> schemas.UserPrivate:
    coins = coins.coins
    if coins < 0:
        raise HTTPException(status_code=400, detail='Coins should be positive')
    if user.current_energy < coins:
        raise HTTPException(status_code=400, detail='Not enough energy')
    crud.users.update_user_money(db, user, coins)
    crud.users.decrease_user_energy(db, user, coins)
    if user.club_id:
        crud.clubs.update_clubs_total_coins(db, user.club_id, coins)
    return user


@router.get(
    '/turbo',
    response_model=bool,
    status_code=200,
)
async def get_turbo(user: models.User = Depends(get_user)) -> bool:
    return user.turbo_available


@router.get(
    '/collectTurboCoins',
    response_model=schemas.UserPrivate,
    status_code=200,
    responses={
        400: {'description': 'Turbo not available'},
    },
)
async def collect_turbo_coins(
    coins: Annotated[int, Body(ge=0, le=200)],
    db=Depends(get_db),
    user: models.User = Depends(get_user)
) -> schemas.UserPrivate:
    if not user.turbo_available:
        raise HTTPException(status_code=400, detail='Turbo not available')

    crud.users.update_user_money(db, user, coins)
    if user.club_id:
        crud.clubs.update_clubs_total_coins(db, user.club_id, coins)
    user = crud.users.update_user_turbo(db, user, False)

    return user
