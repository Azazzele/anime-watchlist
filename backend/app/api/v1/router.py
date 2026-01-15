from fastapi import APIRouter
from .endpoints import media, season, characters

api_router = APIRouter()


api_router.include_router(media.router, tags=["media"])
api_router.include_router(season.router) 
api_router.include_router(characters.router, tags=["characters"])

