from fastapi import Request, APIRouter, Depends, HTTPException
from database import crud, schemas, models
from sqlalchemy.orm import Session
from dependencies import get_db, get_user

router = APIRouter(prefix='/boosts')


@router.get(
    '/',
    response_model=list[schemas.Boost],
    status_code=200,
)
async def get_rating(
    user: models.User = Depends(get_user),
) -> list[schemas.Boost]:
    return user.boosts


@router.post(
    '/buy/{boost_id}',
    response_model=schemas.UserPrivate,
    status_code=200,
    responses={404: {'description': 'Boost not found'}, 400: {'description': 'Not enough coins'}},
)
async def buy_boost(
    boost_id: int,
    user: models.User = Depends(get_user),
    db: Session = Depends(get_db),
):
    boost = crud.boosts.get_boost(db, boost_id)
    if not boost:
        raise HTTPException(status_code=404, detail='Boost not found')

    # multiply by count
    print(user.boosts[0].count)
    if user.current_coins < boost.base_price * X:
        raise HTTPException(status_code=400, detail='Not enough coins')

    crud.boosts.buy_boost(db, user.tg_id, boost_id)
    return


@router.post(
    '/use/{boost_id}',
    response_model=schemas.UserPrivate,
    status_code=200,
    responses={404: {'description': 'Boost not found'}, 400: {'description': 'Not enough boosts'}},
)
async def use_boost(
    boost_id: int,
    user: models.User = Depends(get_user),
    db: Session = Depends(get_db),
):
    free_boosts = ['free_turbo', 'free_refills']
    if boost_id not in range(len(free_boosts)):
        raise HTTPException(status_code=404, detail='Boost not found')

    if boost_id == 0:
        if user.free_turbo < 1:
            raise HTTPException(status_code=400, detail='Not enough boosts')
        user = crud.users.user_use_free_turbo(db, user)
    elif boost_id == 1:
        if user.free_refills < 1:
            raise HTTPException(status_code=400, detail='Not enough boosts')
        user = crud.users.user_use_free_refill(db, user)
    return user


