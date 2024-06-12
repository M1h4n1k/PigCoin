from fastapi import Request, APIRouter, Depends, HTTPException
from database import crud, schemas, models
from sqlalchemy.orm import Session
from dependencies import get_db, get_user

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
    response_model=schemas.Club,
    status_code=201,
)
async def create_club(
    club_tag: str,
    db: Session = Depends(get_db),
) -> schemas.Club:
    # research telegram api for getting public channels
    ...


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


@router.get(
    '/{club_id}/members',
    response_model=list[schemas.UserPublic],
    status_code=200,
    responses={404: {'description': 'Club not found'}},
)
async def get_club_members(
    club_id: int,
    db: Session = Depends(get_db),
) -> list[schemas.User]:
    club = crud.clubs.get_club(db, club_id)
    if not club:
        raise HTTPException(status_code=404, detail='Club not found')
    return club.members

