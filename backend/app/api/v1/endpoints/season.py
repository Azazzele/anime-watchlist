from datetime import datetime, timezone
from enum import Enum
from typing import List
import logging
import random

from fastapi import APIRouter

from app.core.graphql import gql
from app.models.responses import MediaShort
from app.services.anilist_service import anilist_query


# GraphQL queries
CURRENT_SEASON_QUERY = gql("current_season")


# Enums
class MediaSeasonEnum(str, Enum):
    WINTER = "WINTER"
    SPRING = "SPRING"
    SUMMER = "SUMMER"
    FALL = "FALL"


# Router
router = APIRouter(
    prefix="/season",
    tags=["season"],
)

logger = logging.getLogger(__name__)


@router.get(
    "/current",
    response_model=List[MediaShort],
)
@router.get(
    "/current",
    response_model=List[MediaShort],
)
async def get_current_season_anime(limit: int = 8) -> List[MediaShort]:
    now = datetime.now(timezone.utc)
    year = now.year
    month = now.month

    if month in (1, 2, 3):
        season = MediaSeasonEnum.WINTER
    elif month in (4, 5, 6):
        season = MediaSeasonEnum.SPRING
    elif month in (7, 8, 9):
        season = MediaSeasonEnum.SUMMER
    else:
        season = MediaSeasonEnum.FALL

    all_media: list[dict] = []
    page = 1
    per_page = 50  # максимум AniList

    try:
        while True:
            variables = {
                "season": season.value,
                "seasonYear": year,
                "perPage": per_page,
                "page": page,
            }

            data = await anilist_query(
                CURRENT_SEASON_QUERY,
                variables,
            )

            page_data = data.get("Page", {})
            media = page_data.get("media", [])

            if not media:
                break

            all_media.extend(media)

            if not page_data.get("pageInfo", {}).get("hasNextPage"):
                break

            page += 1

        if not all_media:
            logger.warning(
                "No media found for %s %s",
                season.value,
                year,
            )
            return []

        # 🔀 НАСТОЯЩИЙ РАНДОМ
        random.shuffle(all_media)

        # ✂️ ЛИМИТ
        selected = all_media[:limit]

        return [
            MediaShort.model_validate(item)
            for item in selected
        ]

    except Exception:
        logger.exception("Error fetching current season anime")
        return []
