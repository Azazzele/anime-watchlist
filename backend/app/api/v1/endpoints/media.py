from typing import Optional
import logging

from fastapi import APIRouter, HTTPException, Path

from app.core.graphql import gql
from app.models.responses import FullAnimeDetails
from app.services.anilist_service import anilist_query


# GraphQL queries
ANIME_DETAILS_QUERY = gql("anime_details")


# Router
router = APIRouter(
    tags=["anime"],
)

logger = logging.getLogger(__name__)


@router.get(
    "/anime/{media_id}",
    response_model=FullAnimeDetails,
)
async def get_media_details(
    media_id: int = Path(..., ge=1),
) -> FullAnimeDetails:
    try:
        data = await anilist_query(
            ANIME_DETAILS_QUERY,
            {"id": media_id},
        )

        media = data.get("Media")

        if not media:
            logger.warning(
                "Anime not found: media_id=%s",
                media_id,
            )
            raise HTTPException(
                status_code=404,
                detail="Аниме не найдено",
            )

        return FullAnimeDetails.model_validate(media)

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Error fetching anime details: media_id=%s",
            media_id,
        )
        raise HTTPException(
            status_code=503,
            detail="Не удалось загрузить данные аниме с AniList",
        )
