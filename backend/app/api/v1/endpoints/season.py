from datetime import datetime, timezone
from enum import Enum
from typing import List
import logging
import random

from fastapi import APIRouter, HTTPException, Query, status

from app.core.graphql import gql
from app.models.responses import MediaShort
from app.services.anilist_service import anilist_query

CURRENT_SEASON_QUERY = gql("current_season")

logger = logging.getLogger(__name__)


class MediaSeasonEnum(str, Enum):
    WINTER = "WINTER"
    SPRING = "SPRING"
    SUMMER = "SUMMER"
    FALL = "FALL"


router = APIRouter(
    prefix="/season",
    tags=["season"],
)


@router.get("/current", response_model=List[MediaShort])
async def get_current_season_anime(
    limit: int = Query(8, ge=1, le=50)
) -> List[MediaShort]:

    now = datetime.now(timezone.utc)
    month = now.month
    year = now.year   # ✅ ВАЖНО

    if month in (1, 2, 3):
        season = MediaSeasonEnum.WINTER
    elif month in (4, 5, 6):
        season = MediaSeasonEnum.SPRING
    elif month in (7, 8, 9):
        season = MediaSeasonEnum.SUMMER
    else:
        season = MediaSeasonEnum.FALL

    variables = {
        "season": season.value,
        "seasonYear": year,
        "perPage": 50,
        "page": 1,
    }

    logger.debug(f"Season query vars: {variables}")

    try:
        result = await anilist_query(CURRENT_SEASON_QUERY, variables)

        data = result.get("data", {})
        page = data.get("Page", {})
        media = page.get("media", [])

        if not media:
            logger.warning("No media for %s %s", season.value, year)
            return []

        # fallback coverImage
        for item in media:
            if not item.get("coverImage"):
                item["coverImage"] = {
                    "large": f"https://img.anili.st/media/{item['id']}",
                    "extraLarge": f"https://img.anili.st/media/{item['id']}",
                }

        random.shuffle(media)
        selected = media[:limit]

        return [MediaShort.model_validate(item) for item in selected]

    except RuntimeError as e:
        logger.error("AniList error (current season): %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Ошибка при запросе к AniList"
        )

    except Exception:
        logger.exception("Internal error /season/current")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )
