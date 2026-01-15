from pydantic import BaseModel, computed_field
from typing import Optional, Literal, List

class CoverImage(BaseModel):
    extraLarge: Optional[str] = None
    large: Optional[str] = None
    medium: Optional[str] = None

class Title(BaseModel):
    romaji: Optional[str] = None
    english: Optional[str] = None

class CharacterBirthday(BaseModel):
    id: int
    name_full: str
    name_native: str | None = None
    image_large: str | None = None
    favourites: int | None = None
    anime_title_romaji: str | None = None
    anime_title_english: str | None = None  

class FullAnimeDetails(BaseModel):
    id: int
    title: Title
    type: Literal["ANIME", "MANGA"]
    format: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    season: Optional[str] = None
    seasonYear: Optional[int] = None
    episodes: Optional[int] = None
    duration: Optional[int] = None
    averageScore: Optional[int] = None
    popularity: Optional[int] = None
    favourites: Optional[int] = None
    coverImage: Optional[CoverImage] = None
    bannerImage: Optional[str] = None
    genres: List[str] = []
    studios: dict = {} 
    characters: dict = {}  

    @computed_field
    @property
    def cover_image_url(self) -> str:
        if self.coverImage:
            url = self.coverImage.extraLarge or self.coverImage.large or self.coverImage.medium
            if url:
                return url
        return f"https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx{self.id}.png"

class MediaShort(BaseModel):
    id: int
    title: Title
    type: Literal["ANIME", "MANGA"]
    format: Optional[str] = None
    seasonYear: Optional[int] = None
    averageScore: Optional[int] = None
    coverImage: Optional[CoverImage] = None

    @computed_field
    @property
    def cover_image_url(self) -> str:
        """Всегда возвращает рабочий URL постера"""
        if self.coverImage:
                    url = self.coverImage.extraLarge or self.coverImage.large or self.coverImage.medium
                    if url:
                        return url
                # Fallback на лучший CDN AniList
        return f"https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx{self.id}.png"