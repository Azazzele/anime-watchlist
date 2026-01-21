from fastapi import APIRouter, HTTPException, status, Depends
import logging

from app.core.graphql import gql
from app.services.anilist_service import anilist_query
from app.models.responses import (
    UserProfile,
    Avatar,
    UserStatistics,
    AnimeStats,
    MangaStats,
    UserFavourites,
    MediaMini,
    CharacterMini,
    TitleShort,
    CoverImage,
    NameFull,
    StaffImage,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/user", tags=["User"])

# ─────────────────────────────────────────────────────────────
# GraphQL queries
# ─────────────────────────────────────────────────────────────

USER_PROFILE_QUERY = gql("user_profile")
VIEWER_PROFILE_QUERY = gql("viewer_profile")

# ─────────────────────────────────────────────────────────────
# Auth dependency (заглушка, замени на свою)
# ─────────────────────────────────────────────────────────────

async def get_current_token() -> str:
    # TODO: JWT / OAuth / Session
    return "access_token"

# ─────────────────────────────────────────────────────────────
# MAPPERS (ЕДИНЫЙ ИСТОЧНИК ПРАВДЫ)
# ─────────────────────────────────────────────────────────────

def map_media(item: dict) -> MediaMini:
    return MediaMini(
        id=item["id"],
        title=TitleShort(**(item.get("title") or {})),
        coverImage=CoverImage(**(item.get("coverImage") or {}))
        if item.get("coverImage") else None,
    )


def map_character(item: dict) -> CharacterMini:
    return CharacterMini(
        id=item["id"],
        name=NameFull(**(item.get("name") or {})),
        image=StaffImage(
            large=item.get("image", {}).get("large")
        ) if item.get("image") else None,
    )


def map_user_profile(user_data: dict) -> UserProfile:
    favourites = user_data.get("favourites", {})

    return UserProfile(
        id=user_data["id"],
        name=user_data["name"],
        avatar=Avatar(**user_data.get("avatar", {}))
        if user_data.get("avatar") else None,
        bannerImage=user_data.get("bannerImage"),
        about=user_data.get("about"),
        statistics=UserStatistics(
            anime=AnimeStats(**user_data["statistics"]["anime"])
            if user_data.get("statistics", {}).get("anime") else None,
            manga=MangaStats(**user_data["statistics"]["manga"])
            if user_data.get("statistics", {}).get("manga") else None,
        ) if user_data.get("statistics") else None,
        favourites=UserFavourites(
            anime=[map_media(a) for a in favourites.get("anime", {}).get("nodes", [])],
            manga=[map_media(m) for m in favourites.get("manga", {}).get("nodes", [])],
            characters=[map_character(c) for c in favourites.get("characters", {}).get("nodes", [])],
            staff=[map_character(s) for s in favourites.get("staff", {}).get("nodes", [])],
        ) if favourites else None,
        createdAt=user_data.get("createdAt"),
        updatedAt=user_data.get("updatedAt"),
        siteUrl=user_data.get("siteUrl"),
        donatorTier=user_data.get("donatorTier"),
        moderatorRoles=user_data.get("moderatorRoles", []),
    )

# ─────────────────────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────────────────────

@router.get("/me", response_model=UserProfile)
async def get_current_user_profile(
    _: str = Depends(get_current_token),
):
    """
    Профиль текущего авторизованного пользователя (Viewer)
    """
    logger.info("Запрос профиля текущего пользователя")

    try:
        response = await anilist_query(
            VIEWER_PROFILE_QUERY,
            variables={}
        )

        user_data = response.get("Viewer")
        if not user_data:
            raise HTTPException(
                status.HTTP_401_UNAUTHORIZED,
                "Не авторизован или профиль недоступен"
            )

        return map_user_profile(user_data)

    except HTTPException:
        raise

    except KeyError as e:
        logger.error(f"Отсутствует ключ в ответе AniList: {e}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Некорректный ответ AniList"
        )

    except Exception:
        logger.exception("Ошибка при получении профиля пользователя")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Ошибка сервера"
        )


@router.get("/{username}", response_model=UserProfile)
async def get_user_profile_by_name(username: str):
    """
    Публичный профиль пользователя по username
    """
    logger.info(f"Запрос публичного профиля пользователя: {username}")

    try:
        response = await anilist_query(
            USER_PROFILE_QUERY,
            variables={"name": username}
        )

        user_data = response.get("User")
        if not user_data:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                "Пользователь не найден"
            )

        return map_user_profile(user_data)

    except HTTPException:
        raise

    except KeyError as e:
        logger.error(f"Отсутствует ключ в ответе AniList: {e}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Некорректный ответ AniList"
        )

    except Exception:
        logger.exception(f"Ошибка при получении профиля пользователя {username}")
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Внутренняя ошибка сервера"
        )
