from fastapi import APIRouter
import logging
from app.core.graphql import gql
from app.services.anilist_service import anilist_query
from app.models.responses import StaffDetails, MediaMini

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/staff", tags=["staff"])

STAFF_BY_ID_QUERY = gql("staff_by_id")


@router.get("/{staff_id}", response_model=StaffDetails)
async def get_staff(staff_id: int):
    try:
        data = await anilist_query(
            STAFF_BY_ID_QUERY,
            {"id": staff_id},
        )

        staff = data.get("Staff")
        if not staff:
            return None

        return StaffDetails(
            id=staff["id"],
            name_full=staff["name"]["full"],
            name_native=staff["name"].get("native"),
            image_large=staff.get("image", {}).get("large"),
            description=staff.get("description"),
            favourites=staff.get("favourites"),
            occupations=staff.get("primaryOccupations", []),
            works=[
                MediaMini(
                    id=m["id"],
                    title=m["title"],
                    coverImage=m.get("coverImage"),
                )
                for m in staff.get("staffMedia", {}).get("nodes", [])
            ],
        )

    except Exception:
        logger.error("Ошибка загрузки персонала", exc_info=True)
        return None
