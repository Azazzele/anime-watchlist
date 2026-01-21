from fastapi import APIRouter, HTTPException, Query, status
from typing import List
import logging

from app.services.anilist_service import anilist_query
from app.models.responses import CharacterBirthday
from app.core.graphql import gql

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/characters", tags=["characters"])

TODAY_BIRTHDAYS_QUERY = gql("today_birthday")


@router.get("/today-birthdays", response_model=List[CharacterBirthday])
async def get_today_birthdays(
    per_page: int = Query(8, ge=1, le=50)
):
    """
    Персонажи, у которых сегодня день рождения (AniList)
    """

    try:
        data = await anilist_query(
            TODAY_BIRTHDAYS_QUERY,
            {
                "perPage": per_page,
                "sort": ["FAVOURITES_DESC"],
            }
        )

        characters = data.get("Page", {}).get("characters", [])

        logger.info("Найдено персонажей с ДР: %s", len(characters))

        result: List[CharacterBirthday] = []

        for char in characters:
            media_nodes = char.get("media", {}).get("nodes") or []
            first_media = media_nodes[0] if media_nodes else {}

            title = first_media.get("title", {})

            result.append(
                CharacterBirthday(
                    id=char["id"],
                    name_full=char["name"]["full"],
                    name_native=char["name"].get("native"),
                    image_large=char.get("image", {}).get("large"),
                    favourites=char.get("favourites"),
                    anime_title_romaji=title.get("romaji"),
                    anime_title_english=title.get("english"),
                )
            )

        return result

    except RuntimeError as e:
        # ошибки AniList (GraphQL, timeout)
        logger.error("AniList error (birthdays): %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Ошибка при запросе к AniList"
        )

    except Exception:
        logger.exception("Внутренняя ошибка /characters/today-birthdays")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )
