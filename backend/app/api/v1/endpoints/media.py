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
    "ranobe": "NOVEL",
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

    gql_type = MEDIA_TYPE_MAP[media_type]

    try:
        result = await anilist_query(
            MEDIA_DETAILS_QUERY,
            {
                "id": media_id,
                "type": gql_type,
            },
        )

        data = result.get("data", {})
        media = data.get("Media")

        if not media:
            raise HTTPException(
                status_code=404,
                detail=f"{media_type.upper()} не найден",
            )

        return FullAnimeDetails.model_validate(media)

    except HTTPException:
        raise

    except Exception:
        logger.exception(
            "Error fetching media: type=%s id=%s",
            media_type,
            media_id,
        )
        raise HTTPException(
            status_code=503,
            detail="Ошибка загрузки данных AniList",
        )
