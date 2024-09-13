import re
from fastapi import Request, APIRouter, Depends, HTTPException, Query, Body
from database import crud, schemas, models
from sqlalchemy.orm import Session
from dependencies import get_db, get_user
from typing import Annotated

from bot import bot
from utils import load_image


router = APIRouter(prefix='/clubs')


@router.get(
    '/{club_id}',
    response_model=schemas.Club,
    status_code=200,
    responses={404: {'description': 'Club not found'}},
)
async def get_rating(
    club_id: int,
    db: Session = Depends(get_db),
) -> schemas.Club:
    club = crud.clubs.get_club(db, club_id)
    if not club:
        raise HTTPException(status_code=404, detail='Club not found')
    return club


@router.post(
    '/',
    response_model=schemas.UserPrivate,
    status_code=201,
)
async def create_club(
    club_tag: str = Body(...),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_user),
):
    if re.match(r'[^a-zA-Z0-9_]', club_tag):
        raise HTTPException(status_code=400, detail='Invalid club tag')
    if user.club_id:
        raise HTTPException(status_code=400, detail='User already in club')
    club = crud.clubs.get_club_by_name(db, club_tag)

    if not club:
        try:
            channel = await bot.get_chat('@' + club_tag)
        except Exception:
            raise HTTPException(status_code=404, detail='Channel not found')
        if not channel:
            raise HTTPException(status_code=404, detail='Channel not found')

        picture_path = '/pig_ava.png'
        if channel.photo:
            picture_path = await load_image(channel.photo.small_file_id, channel.id)

        club = models.Club(
            id=channel.id,
            name=channel.title,
            picture=picture_path,
            tg_tag=club_tag,
            creator_tg_id=user.tg_id,
            total_coins=0,
            members_count=0,
        )
        club = crud.clubs.create_club(db, club)

    crud.users.update_user_club(db, user, club.id)

    return user


@router.post(
    '/{club_id}/join',
    response_model=schemas.Club,
    status_code=200,
    responses={404: {'description': 'Club or user not found'}},
)
async def join_club(
    club_id: int,
    user: models.User = Depends(get_user),
    db: Session = Depends(get_db),
) -> schemas.Club:
    club = crud.clubs.get_club(db, club_id)
    if not club:
        raise HTTPException(status_code=404, detail='Club not found')
    crud.users.update_user_club(db, user, club_id)

    return club


@router.delete(
    '/leave',
    response_model=schemas.UserPrivate,
    status_code=200,
    responses={404: {'description': 'Club or user not found'}},
)
async def leave_club(
    user: models.User = Depends(get_user),
    db: Session = Depends(get_db),
):
    if not user.club_id:
        raise HTTPException(status_code=404, detail='User not in club')
    crud.users.update_user_club(db, user, None)

    return user


@router.get(
    '/{club_id}/members',
    response_model=list[schemas.UserPublic],
    status_code=200,
    responses={404: {'description': 'Club not found'}},
)
async def get_club_members(
    club_id: int,
    db: Session = Depends(get_db),
    offset: int = 0,
    limit: Annotated[int, Query(..., le=100)] = 10
) -> list[schemas.User]:
    club = crud.clubs.get_club(db, club_id)
    if not club:
        raise HTTPException(status_code=404, detail='Club not found')
    return club.members.offset(offset).limit(limit).all()

