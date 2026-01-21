from fastapi import APIRouter

from .endpoints.media import router as media_router
from .endpoints.season import router as season_router
from .endpoints.characters import router as characters_router
from .endpoints.character import router as character_router
from .endpoints.staff import router as staff_router
from .endpoints.user import router as user

api_router = APIRouter()

# Подключаем все роутеры
api_router.include_router(media_router)
api_router.include_router(season_router)
api_router.include_router(characters_router)
api_router.include_router(character_router)
api_router.include_router(staff_router)
api_router.include_router(user, tags=["User"])