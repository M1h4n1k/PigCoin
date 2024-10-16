from fastapi import APIRouter, Depends, HTTPException, Body
import asyncio
from apscheduler.triggers.date import DateTrigger
from database import crud, schemas, models
from database.loader import scheduler, SessionLocal
from sqlalchemy.orm import Session
from dependencies import get_db, get_user
from datetime import datetime
import logging
from bot import bot

router = APIRouter(prefix='/decorations', responses={404: {'description': 'User not found'}})


def wrapper_finish_auction(decoration_id: int):
    asyncio.run(finish_auction(decoration_id))


async def finish_auction(decoration_id: int):
    db = SessionLocal()
    decoration = crud.decorations.get_decoration_by_id(db, decoration_id)
    crud.decorations.finish_auction(db, decoration)
    await bot.send_message(decoration.last_bet_user.tg_id, f'Ваш выигрыш на аукционе {decoration.title}!')
    db.close()


@router.post(
    '/bet',
    response_model=schemas.Decoration,
    status_code=200,
    responses={
        400: {'description': 'Decoration not found'},
        403: {'description': 'Auction has ended'},
        412: {'description': 'Not enough coins'},
        406: {'description': 'Bet must be higher than last bet'},

    }
)
async def bet_decoration(
    decoration_id: int = Body(...),
    amount: int = Body(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user),
):
    decoration = crud.decorations.get_decoration_by_id(db, decoration_id)
    if not decoration:
        raise HTTPException(status_code=400, detail='Decoration not found')
    if decoration.betting_ends_at < datetime.now():
        raise HTTPException(status_code=403, detail='Auction has ended')
    if user.current_coins < amount:
        raise HTTPException(status_code=412, detail='Not enough coins')
    if amount <= decoration.last_bet:
        raise HTTPException(status_code=406, detail='Bet must be higher than last bet')
    logging.info(f'{user.tg_id}:{user.username} bet {amount} on decoration {decoration.id}')

    updated_decoration = crud.decorations.make_bet(db, user, decoration, amount)
    date_trigger = DateTrigger(run_date=updated_decoration.betting_ends_at)
    job_id = f'decoration_auction_{updated_decoration.id}'
    if scheduler.get_job(job_id):
        scheduler.reschedule_job(job_id, trigger=date_trigger)
    else:
        scheduler.add_job(wrapper_finish_auction, trigger=date_trigger, args=(updated_decoration.id,), id=job_id)

    return updated_decoration


@router.get(
    '/',
    response_model=schemas.Decoration | None,  # for now, I think that only one decoration can on the auction
    status_code=200,
)
async def get_decoration(db: Session = Depends(get_db)):
    return crud.decorations.get_decoration_on_auction(db)
