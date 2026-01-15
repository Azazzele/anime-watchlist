from fastapi import APIRouter
from app.services.anilist_service import anilist_query
from app.models.responses import MediaShort
from typing import List
from enum import Enum
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class MediaSeasonEnum(str, Enum):
    WINTER = "WINTER"
    SPRING = "SPRING"
    SUMMER = "SUMMER"
    FALL = "FALL"

router = APIRouter(prefix="/season", tags=["season"])
CURRENT_SEASON_QUERY = """
query ($season: MediaSeason, $seasonYear: Int, $perPage: Int) {
  Page(page: 1, perPage: $perPage) {
    media(
      type: ANIME
      season: $season
      seasonYear: $seasonYear
      sort: POPULARITY_DESC
    ) {
      id
      title {
        romaji
        english
      }
      format
      coverImage {
        large
        extraLarge
      }
      type
      averageScore
      seasonYear
      status               
    }
  }
}
"""
@router.get("/current", response_model=List[MediaShort])
async def get_current_season_anime(limit: int = 8):
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

    variables = {
        "season": season.value,
        "seasonYear": year,
        "perPage": limit
    }

    try:
          data = await anilist_query(CURRENT_SEASON_QUERY, variables)
          media_list = data.get("Page", {}).get("media") or []

          if not media_list:
              return []  # или сообщение, если хочешь

          # Pydantic сам всё заполнит, включая cover_image_url
          return [MediaShort.model_validate(item) for item in media_list]

    except Exception as e:
        logger.error("Season fetch error", exc_info=True)
        return []