from fastapi import APIRouter
from datetime import datetime
from typing import List
from app.services.anilist_service import anilist_query
from app.models.responses import CharacterBirthday
import logging
from app.core.graphql import gql


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/characters", tags=["characters"])

TODAY_BIRTHDAYS_QUERY = gql("today_bithday")

@router.get("/today-birthdays", response_model=List[CharacterBirthday])
async def get_today_birthdays(per_page: int = 8):
    today = datetime.now()
    month = today.month
    day = today.day

    variables = {
        "perPage": per_page,
        "sort": ["FAVOURITES_DESC"]
    }

    try:
        data = await anilist_query(TODAY_BIRTHDAYS_QUERY, variables)
        characters = data.get("Page", {}).get("characters") or []

        logger.info(f"Найдено персонажей с ДР {month}-{day}: {len(characters)}")

        return [
            CharacterBirthday(
                id=char["id"],
                name_full=char["name"]["full"],
                name_native=char["name"].get("native"),
                image_large=char.get("image", {}).get("large"),
                favourites=char.get("favourites"),
                anime_title_romaji=(
                    char.get("media", {})
                        .get("nodes", [{}])[0]
                        .get("title", {})
                        .get("romaji")
                ),
                anime_title_english=(
                    char.get("media", {})
                        .get("nodes", [{}])[0]
                        .get("title", {})
                        .get("english")
                )
            )
            for char in characters
        ]

    except Exception as e:
        logger.error(f"Ошибка загрузки ДР персонажей: {str(e)}", exc_info=True)
        return []