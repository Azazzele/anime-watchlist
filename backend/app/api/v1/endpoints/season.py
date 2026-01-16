from datetime import datetime, timezone
from enum import Enum
from typing import List
import logging

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
async def get_current_season_anime(limit: int = 8) -> List[MediaShort]:
    now = datetime.now(timezone.utc)
    year = now.year
    month = now.month

    # Determine season (AniList rules)
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
        "perPage": limit,
        "page": 1,
    }

    try:
        data = await anilist_query(
            CURRENT_SEASON_QUERY,
            variables,
        )

        media_list = data.get("Page", {}).get("media", [])

        if not media_list:
            logger.warning(
                "No media found for %s %s",
                season.value,
                year,
            )
            return []

        # Pydantic fills computed fields automatically
        return [
            MediaShort.model_validate(item)
            for item in media_list
        ]

    except Exception:
        logger.exception("Error fetching current season anime")
        return []