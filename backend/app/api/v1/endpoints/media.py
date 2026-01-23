from fastapi import APIRouter, HTTPException, Path
import logging

from app.core.graphql import gql
from app.services.anilist_service import anilist_query
from app.models.responses import FullAnimeDetails

router = APIRouter(
    prefix="",
    tags=["media"],
)

logger = logging.getLogger(__name__)

MEDIA_DETAILS_QUERY = gql("media_details")

MEDIA_TYPE_MAP = {
    "anime": "ANIME",
    "manga": "MANGA",
    "ranobe": "MANGA",
}


@router.get(
    "/media/{media_type}/{media_id}",
    response_model=FullAnimeDetails,
)
async def get_media_details(
    media_type: str,
    media_id: int = Path(..., ge=1),
):
    media_type = media_type.lower()

    if media_type not in MEDIA_TYPE_MAP:
        raise HTTPException(
            status_code=400,
            detail="Неверный тип медиа (anime | manga | ranobe)",
        )

    expected_type = MEDIA_TYPE_MAP[media_type]

    try:
        result = await anilist_query(
            MEDIA_DETAILS_QUERY,
            {"id": media_id},
        )

        media = result.get("data", {}).get("Media")
        
        if not media:
            raise HTTPException(
                status_code=404,
                detail="Медиа не найдено",
            )

        if media.get("type") != expected_type:
            raise HTTPException(
                status_code=400,
                detail=f"Это не {media_type.upper()}",
            )

        return FullAnimeDetails.model_validate(media)

    except HTTPException:
        raise

    except Exception:
        logger.exception("AniList error")
        raise HTTPException(
            status_code=503,
            detail="Ошибка загрузки данных AniList",
        )
