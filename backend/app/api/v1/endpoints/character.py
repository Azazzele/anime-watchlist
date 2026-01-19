from fastapi import APIRouter, HTTPException, status
import logging
from app.core.graphql import gql
from app.services.anilist_service import anilist_query
from app.models.responses import (
    CharacterDetails,
    Title,
    CoverImage,
    MediaMini,
    DateOfBirth
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/character")

CHARACTER_BY_ID_QUERY = gql("character")


@router.get("/{character_id}", response_model=CharacterDetails)
async def get_character(character_id: int):
    try:
        response = await anilist_query(
            CHARACTER_BY_ID_QUERY,
            variables={"id": character_id}
        )

        if "errors" in response:
            logger.warning(f"AniList error for character {character_id}: {response['errors']}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Ошибка внешнего API AniList"
            )

        char_data = response.get("Character")
        if not char_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Персонаж не найден"
            )

        return CharacterDetails(
            id=char_data["id"],
            name_full=char_data["name"].get("full", "—"),
            name_native=char_data["name"].get("native"),
            name_alternative=char_data["name"].get("alternative", []),
            image_large=char_data.get("image", {}).get("large"),
            description=char_data.get("description"),
            favourites=char_data.get("favourites"),

            age=char_data.get("age"),
            gender=char_data.get("gender"),
            bloodType=char_data.get("bloodType"),

            dateOfBirth=DateOfBirth(**char_data["dateOfBirth"])
            if char_data.get("dateOfBirth") else None,

            anime=[
                MediaMini(
                    id=media["id"],
                    title=Title(**media["title"]),
                    coverImage=CoverImage(**media["coverImage"])
                    if media.get("coverImage") else None,

                    format=media.get("format"),
                    seasonYear=media.get("seasonYear"),
                    averageScore=media.get("averageScore"),
                )
                for media in char_data.get("media", {}).get("nodes", [])
            ]
        )

    except Exception:
        logger.error("Ошибка при получении персонажа", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )
