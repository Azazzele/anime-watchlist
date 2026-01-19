from pydantic import BaseModel, computed_field
from typing import Optional, Literal, List

class CoverImage(BaseModel):
    extraLarge: Optional[str] = None
    large: Optional[str] = None
    medium: Optional[str] = None

class StaffName(BaseModel):
    full: Optional[str] = None
    native: Optional[str] = None


class StaffImage(BaseModel):
    large: Optional[str] = None


class StaffNode(BaseModel):
    id: int
    name: StaffName
    image: Optional[StaffImage] = None


class StaffEdge(BaseModel):
    role: str
    node: StaffNode


class Staff(BaseModel):
    edges: List[StaffEdge] = []


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

class RelationTitle(BaseModel):
    romaji: Optional[str] = None
    english: Optional[str] = None


class RelationCoverImage(BaseModel):
    large: Optional[str] = None


class RelationStartDate(BaseModel):
    year: Optional[int] = None


class RelationNode(BaseModel):
    id: int
    type: Optional[str] = None
    format: Optional[str] = None
    title: RelationTitle
    coverImage: Optional[RelationCoverImage] = None
    startDate: Optional[RelationStartDate] = None


class RelationEdge(BaseModel):
    relationType: str
    node: RelationNode


class Relations(BaseModel):
    edges: List[RelationEdge] = []

class Trailer(BaseModel):
    id: str                     
    site: Literal["youtube", "dailymotion"] = "youtube"
    thumbnail: Optional[str] = None


class StreamingEpisode(BaseModel):
    title: Optional[str] = None
    thumbnail: Optional[str] = None      
    url: Optional[str] = None
    site: Optional[str] = None       

class FullAnimeDetails(BaseModel):
    id: int
    title: Title
    type: Literal["ANIME", "MANGA"]
    staff: Optional[Staff] = None
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
    trailer: Optional[Trailer] = None
    streamingEpisodes: List[StreamingEpisode] = []
    relations: Optional[Relations] = None

    @computed_field
    @property
    def cover_image_url(self) -> str:
        if self.coverImage:
            url = (
                self.coverImage.extraLarge
                or self.coverImage.large
                or self.coverImage.medium
            )
            if url:
                return url

        return (
            f"https://s4.anilist.co/file/anilistcdn/media/anime/"
            f"cover/large/bx{self.id}.png"
        )
    @computed_field
    @property
    def youtube_trailer_url(self) -> Optional[str]:
        """Готовый embed URL для <iframe>"""
        if not self.trailer:
            return None
        if self.trailer.site == "youtube":
            return f"https://www.youtube.com/embed/{self.trailer.id}"
        # можно добавить поддержку dailymotion и других
        return None

    @computed_field
    @property
    def episode_screenshots(self) -> List[str]:
        """Просто список всех доступных скриншотов эпизодов"""
        return [
            ep.thumbnail
            for ep in self.streamingEpisodes
            if ep.thumbnail
        ]
    
class MediaShort(BaseModel):
    id: int

    title: Title

    type: Literal["ANIME", "MANGA"]

    format: Optional[str] = None          # TV / MOVIE / OVA
    status: Optional[str] = None          # RELEASING / FINISHED
    season: Optional[str] = None          
    seasonYear: Optional[int] = None

    averageScore: Optional[int] = None
    popularity: Optional[int] = None

    coverImage: Optional[CoverImage] = None

    @computed_field
    @property
    def cover_image_url(self) -> str:
        """Всегда валидный постер"""
        if self.coverImage:
            url = (
                self.coverImage.extraLarge
                or self.coverImage.large
                or self.coverImage.medium
            )
            if url:
                return url

        return (
            f"https://s4.anilist.co/file/anilistcdn/media/anime/"
            f"cover/large/bx{self.id}.png"
        )
