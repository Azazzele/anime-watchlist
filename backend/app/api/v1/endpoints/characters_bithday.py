from fastapi import APIRouter, HTTPException, Query, status
from typing import List
import logging
from datetime import date

from app.services.anilist_service import anilist_query
from app.models.responses import CharacterBirthday
from app.core.graphql import gql

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/characters", tags=["characters"])

TODAY_BIRTHDAYS_QUERY = gql("today_birthday")

# сколько отдаём клиенту
USER_LIMIT_DEFAULT = 8

# сколько тянем за один запрос к AniList
FETCH_PER_PAGE = 50

# сколько страниц максимум просматриваем
MAX_PAGES = 10


@router.get("/today-birthdays", response_model=List[CharacterBirthday])
async def get_today_birthdays(
    per_page: int = Query(USER_LIMIT_DEFAULT, ge=1, le=50)
):
    """
    Персонажи, у которых сегодня день рождения (AniList)
    """
    today = date.today()

    page = 1
    result: List[CharacterBirthday] = []

    try:
        while page <= MAX_PAGES and len(result) < per_page:
            data = await anilist_query(
                TODAY_BIRTHDAYS_QUERY,
                {
                    "page": page,
                    "perPage": FETCH_PER_PAGE,
                    "sort": ["FAVOURITES_DESC"],
                }
            )

            characters = data.get("Page", {}).get("characters", [])
            logger.info("Page %s: получено персонажей %s", page, len(characters))

            if not characters:
                break

            for char in characters:
                if len(result) >= per_page:
                    break

                dob = char.get("dateOfBirth")
                if not dob:
                    continue

                if dob.get("month") != today.month or dob.get("day") != today.day:
                    continue

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

            page += 1

        logger.info("Найдено именинников сегодня: %s", len(result))
        return result

    except RuntimeError as e:
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
