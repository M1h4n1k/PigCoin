from fastapi import APIRouter
from .user import router as user_router
from .rating import router as rating_router
from .tasks import router as tasks_router
from .clubs import router as clubs_router
from .boosts import router as boosts_router
from .game import router as game_router
from .transactions import router as transactions_router

router = APIRouter(prefix='/api')
routers = [user_router, rating_router, tasks_router, clubs_router, boosts_router, game_router, transactions_router]
for r in routers:
    router.include_router(r)


__all__ = ['router']
