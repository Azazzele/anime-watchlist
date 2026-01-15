from fastapi import APIRouter, Path, HTTPException
from app.models.responses import FullAnimeDetails
from app.services.anilist_service import anilist_query

router = APIRouter()

@router.get("/anime/{media_id}", response_model=FullAnimeDetails)
async def get_media_details(media_id: int = Path(..., ge=1)):
    query = """
    query ($id: Int!) {
      Media(id: $id, type: ANIME) {
        id
        title {
          romaji
          english
          native
        }
        type
        format
        status
        description(asHtml: false)
        season
        seasonYear
        episodes
        duration
        averageScore
        popularity
        favourites
        coverImage {
          extraLarge
          large
          medium
        }
        bannerImage
        genres
        studios(isMain: true) {
          nodes {
            name
          }
        }
        characters(perPage: 12) {
          edges {
            node {
              id
              name {
                full
                native
              }
              image {
                large
              }
            }
            role
          }
        }
      }
    }
    """

    try:
        data = await anilist_query(query, {"id": media_id})
        media = data.get("Media")

        if not media:
            raise HTTPException(status_code=404, detail="Аниме не найдено")

        return FullAnimeDetails.model_validate(media)

    except Exception as e:
        if "not found" in str(e).lower() or "invalid id" in str(e).lower():
            raise HTTPException(status_code=404, detail="Аниме не найдено")
        raise HTTPException(
            status_code=503,
            detail="Не удалось загрузить данные аниме с AniList"
        )