from fastapi import APIRouter, HTTPException, status, Query
import logging
from typing import List

from app.core.graphql import gql
from app.services.anilist_service import anilist_query
from app.models.responses import (
    StaffDetails,
    Title,
    CoverImage,
    StaffMediaMini,
    DateOfBirth
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/staff", tags=["Staff"])

STAFF_BY_ID_QUERY = gql("staff")


@router.get("/{staff_id}", response_model=StaffDetails)
async def get_staff(
    staff_id: int,
    page: int = Query(1, ge=1),
    limit: int = Query(12, ge=1, le=50)
):
    logger.info("GET /staff/%s?page=%s&limit=%s", staff_id, page, limit)

    try:
        data = await anilist_query(
            STAFF_BY_ID_QUERY,
            {
                "id": staff_id,
                "page": page,
                "perPage": limit
            }
        )

        staff_data = data.get("Staff")
        if not staff_data:
            logger.warning("Staff %s not found", staff_id)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Сэйю / стафф не найден"
            )

        staff_media = staff_data.get("staffMedia") or {}
        nodes = staff_media.get("nodes") or []
        page_info = staff_media.get("pageInfo") or {}

        works: List[StaffMediaMini] = []

        for node in nodes:
            cover = node.get("coverImage") or {}

            cover_image = (
                CoverImage(**cover)
                if cover
                else CoverImage(
                    large=f"https://img.anili.st/media/{node['id']}",
                    medium=f"https://img.anili.st/media/{node['id']}"
                )
            )

            title_raw = node.get("title") or {}
            title = Title(
                romaji=title_raw.get("romaji"),
                english=title_raw.get("english")
            )

            works.append(
                StaffMediaMini(
                    id=node["id"],
                    title=title,
                    coverImage=cover_image,
                    format=node.get("format"),
                    seasonYear=node.get("seasonYear"),
                    averageScore=node.get("averageScore"),
                )
            )

        dob_raw = staff_data.get("dateOfBirth")
        dob = DateOfBirth(**dob_raw) if dob_raw else None

        dod_raw = staff_data.get("dateOfDeath")
        dod = DateOfBirth(**dod_raw) if dod_raw else None

        return StaffDetails(
            id=staff_data["id"],
            name_full=staff_data.get("name", {}).get("full", "—"),
            name_native=staff_data.get("name", {}).get("native"),
            name_alternative=staff_data.get("name", {}).get("alternative", []),
            image_large=staff_data.get("image", {}).get("large"),
            description=staff_data.get("description"),
            primary_occupations=staff_data.get("primaryOccupations", []),
            gender=staff_data.get("gender"),
            date_of_birth=dob,
            date_of_death=dod,
            age=staff_data.get("age"),
            years_active=staff_data.get("yearsActive", []),
            home_town=staff_data.get("homeTown"),
            blood_type=staff_data.get("bloodType"),
            favourites=staff_data.get("favourites"),
            works=works,
            works_total=page_info.get("total", 0),
            works_has_next=page_info.get("hasNextPage", False)
        )

    except RuntimeError as e:
        logger.error("AniList error (staff %s): %s", staff_id, str(e))
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Ошибка при запросе к AniList"
        )

    except Exception:
        logger.exception("Внутренняя ошибка /staff/%s", staff_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )
