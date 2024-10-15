from database import crud, schemas, models
from dependencies import get_db, get_user
from fastapi import Query, APIRouter, Depends, HTTPException
import re
from sqlalchemy.orm import Session
from typing import Annotated


router = APIRouter(prefix='/transactions', responses={404: {'description': 'User not found'}})


@router.post(
    '/',
    response_model=schemas.Transaction,
    status_code=200,
    responses={
        400: {'description': 'Amount must be positive | Invalid user_uid | Cannot send coins to yourself'},
        402: {'description': 'Not enough coins'},
        404: {'description': 'User not found'},
    }
)
async def make_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user),
):
    if not re.match(r'^-?[\da-f]+$', transaction.to_user_uid):
        raise HTTPException(status_code=400, detail='Invalid user_uid')
    if transaction.amount <= 0:
        raise HTTPException(status_code=400, detail='Amount must be positive')
    if user.current_coins < transaction.amount:
        raise HTTPException(status_code=402, detail='Not enough coins')
    if user.uid == transaction.to_user_uid:
        raise HTTPException(status_code=400, detail='Cannot send coins to yourself')
    to_user = crud.users.get_user_by_uid(db, transaction.to_user_uid)
    if not to_user:
        raise HTTPException(status_code=404, detail='User not found')
    return crud.users.make_transaction(db, user, to_user, transaction.amount)


@router.get(
    '/',
    response_model=list[schemas.Transaction],
    status_code=200,
)
async def get_transactions(
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: Annotated[int, Query(..., le=100)] = 10,
    user: models.User = Depends(get_user),
):
    return crud.users.get_transactions(db, user, offset, limit)
