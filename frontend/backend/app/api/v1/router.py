from fastapi import APIRouter
from .endpoints import media, season, characters, character

api_router = APIRouter()


api_router.include_router(media.router)
api_router.include_router(season.router)
api_router.include_router(character.router) 
api_router.include_router(characters.router) 

