from fastapi import APIRouter, HTTPException, status
import logging
from typing import List
from app.core.graphql import gql
from app.services.anilist_service import anilist_query
from app.models.responses import (
    CharacterDetails,
    VoiceActorDTO,
    Title,
    CoverImage,
    MediaMini,
    DateOfBirth
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/character", tags=["character"])
CHARACTER_BY_ID_QUERY = gql("character")  # твой GraphQL запрос

@router.get("/{character_id}", response_model=CharacterDetails)
async def get_character(character_id: int):
    try:
        response = await anilist_query(
            CHARACTER_BY_ID_QUERY,
            variables={"id": character_id}
        )

        char_data = response.get("Character")
        if not char_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Персонаж не найден"
            )

        # --- Собираем voice actors ---
        voice_actors: List[VoiceActorDTO] = []
        for edge in char_data.get("media", {}).get("edges", []):
            for va in edge.get("voiceActors", []):
                if va and va.get("id"):
                    voice_actors.append(
                        VoiceActorDTO(
                            id=va["id"],
                            name=va.get("name", {}).get("full", "—"),
                            image=va.get("image", {}).get("large"),
                            language=va.get("languageV2"),
                        )
                    )

        # Убираем дубликаты
        seen = set()
        unique_voice_actors = []
        for va in voice_actors:
            if va.id not in seen:
                seen.add(va.id)
                unique_voice_actors.append(va)

        # --- Возвращаем все данные ---
        return CharacterDetails(
            id=char_data["id"],
            name_full=char_data["name"].get("full", "—"),
            name_native=char_data["name"].get("native"),
            name_alternative=char_data["name"].get("alternative", []),
            image_large=char_data.get("image", {}).get("large"),
            description=char_data.get("description"),
            favourites=char_data.get("favourites"),
            age=char_data.get("age"),
            gender=char_data.get("gender"),
            bloodType=char_data.get("bloodType"),
            dateOfBirth=DateOfBirth(**char_data["dateOfBirth"]) if char_data.get("dateOfBirth") else None,
            anime=[
                MediaMini(
                    id=m["id"],
                    title=Title(**m.get("title", {})),
                    coverImage=CoverImage(**m.get("coverImage")) if m.get("coverImage") else None,
                    format=m.get("format"),
                    seasonYear=m.get("seasonYear"),
                    averageScore=m.get("averageScore"),
                )
                for m in char_data.get("media", {}).get("nodes", [])
            ],
            voice_actors=unique_voice_actors  # ← сюда!
        )

    except Exception as e:
        logger.exception(f"Ошибка при получении персонажа {character_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )
