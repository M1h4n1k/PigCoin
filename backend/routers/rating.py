from fastapi import Request, APIRouter, Depends, HTTPException
from database import crud, schemas, models
from sqlalchemy.orm import Session
from dependencies import get_db
from utils import get_user_league_range, get_club_league_range

router = APIRouter(prefix='/rating')


@router.get(
    '/users',
    response_model=list[schemas.UserPublic],
    status_code=200,
)
async def get_user_rating(
    db: Session = Depends(get_db),
    league: int = None
) -> list[schemas.UserPublic]:
    users = crud.users.get_users_within_coins_range(db, *get_user_league_range(league))
    return users


@router.get(
    '/clubs',
    response_model=list[schemas.Club],
    status_code=200,
)
async def get_club_rating(
    db: Session = Depends(get_db),
    league: int = None
) -> list[schemas.Club]:
    clubs = crud.clubs.get_clubs_within_coins_range(db, *get_club_league_range(league))
    return clubs
