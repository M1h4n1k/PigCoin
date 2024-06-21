import re

from fastapi import Request, APIRouter, Depends, HTTPException, Query, Body
from database import crud, schemas, models
from sqlalchemy.orm import Session
from dependencies import get_db, get_user
from typing import Annotated


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
    if re.match(r'^[A-Z0-9_]', club_tag):
        raise HTTPException(status_code=400, detail='Invalid club tag')
    # research telegram api for getting public channels

    club = models.Club(
        id=123,
        name=club_tag,
        picture='https://t.me/club',
        tg_link=f'https://t.me/{club_tag}',
        total_coins=0,
        members_count=0,
    )
    crud.clubs.create_club(db, club)
    crud.users.update_user_club(db, user, club.id)
    crud.clubs.add_member_to_club(db, club.id)
    crud.clubs.update_clubs_total_coins(db, club.id, user.total_coins)

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
    if user.club_id:
        crud.clubs.update_clubs_total_coins(db, user.club_id, user.total_coins * -1)
        crud.clubs.remove_member_from_club(db, user.club_id)
    crud.users.update_user_club(db, user, club_id)
    crud.clubs.add_member_to_club(db, club_id)
    crud.clubs.update_clubs_total_coins(db, club_id, user.total_coins)

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
    club = crud.clubs.get_club(db, user.club_id)
    crud.clubs.update_clubs_total_coins(db, user.club_id, user.total_coins * -1)
    crud.clubs.remove_member_from_club(db, user.club_id)
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

