from pydantic import BaseModel, computed_field, Field
from typing import Optional, Literal, List, Dict, Any


class VoiceActorName(BaseModel):
    full: Optional[str] = None


class VoiceActorImage(BaseModel):
    large: Optional[str] = None


class VoiceActor(BaseModel):
    id: int
    name: VoiceActorName
    image: Optional[VoiceActorImage] = None
    languageV2: Optional[str] = None


class VoiceActorDTO(BaseModel):
    id: int
    name: str
    image: Optional[str] = None
    language: Optional[str] = Field(None, alias="languageV2")


class CoverImage(BaseModel):
    extraLarge: Optional[str] = None
    large: Optional[str] = None
    medium: Optional[str] = None


class StaffName(BaseModel):
    full: Optional[str] = None
    native: Optional[str] = None


class DateOfBirth(BaseModel):
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None


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
    edges: List[StaffEdge] = Field(default_factory=list)


class Title(BaseModel):
    userPreferred: Optional[str] = None
    romaji: Optional[str] = None
    english: Optional[str] = None
    native: Optional[str] = None


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
    edges: List[RelationEdge] = Field(default_factory=list)


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
    type: Optional[Literal["ANIME", "MANGA"]] = "ANIME"
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
    genres: List[str] = Field(default_factory=list)
    studios: Dict[str, Any] = Field(default_factory=dict)
    characters: Dict[str, Any] = Field(default_factory=dict)
    trailer: Optional[Trailer] = None
    streamingEpisodes: List[StreamingEpisode] = Field(default_factory=list)
    relations: Optional[Relations] = None

    @computed_field
    @property
    def cover_image_url(self) -> str:
        """Всегда возвращает постер"""
        if self.coverImage:
            return (
                self.coverImage.extraLarge
                or self.coverImage.large
                or self.coverImage.medium
                or f"https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx{self.id}.png"
            )
        return f"https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx{self.id}.png"

    @computed_field
    @property
    def youtube_trailer_url(self) -> Optional[str]:
        if self.trailer and self.trailer.site == "youtube":
            return f"https://www.youtube.com/embed/{self.trailer.id}"
        return None

    @computed_field
    @property
    def episode_screenshots(self) -> List[str]:
        return [ep.thumbnail for ep in self.streamingEpisodes if ep.thumbnail]


class MediaShort(BaseModel):
    id: int
    title: Title
    type: Optional[Literal["ANIME", "MANGA"]] = "ANIME"
    format: Optional[str] = None
    status: Optional[str] = None
    season: Optional[str] = None
    seasonYear: Optional[int] = None
    averageScore: Optional[int] = None
    popularity: Optional[int] = None
    coverImage: Optional[CoverImage] = None

    @computed_field
    @property
    def cover_image_url(self) -> str:
        if self.coverImage:
            return (
                self.coverImage.extraLarge
                or self.coverImage.large
                or self.coverImage.medium
                or f"https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx{self.id}.png"
            )
        return f"https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx{self.id}.png"


class MediaMini(BaseModel):
    id: int
    title: Title
    coverImage: Optional[CoverImage] = None
    format: Optional[str] = None
    seasonYear: Optional[int] = None
    averageScore: Optional[int] = None


class CharacterDetails(BaseModel):
    id: int
    name_full: str
    name_native: Optional[str] = None
    name_alternative: List[str] = Field(default_factory=list)
    image_large: Optional[str] = None
    description: Optional[str] = None
    favourites: Optional[int] = None
    age: Optional[str] = None
    gender: Optional[str] = None
    bloodType: Optional[str] = None
    dateOfBirth: Optional[DateOfBirth] = None

    anime: List[MediaMini] = Field(default_factory=list)
    anime_total: int = 0
    anime_has_next: bool = False

    voice_actors: List[VoiceActorDTO] = Field(default_factory=list)


class CharacterBirthday(BaseModel):
    id: int
    name_full: str
    name_native: Optional[str] = None
    image_large: Optional[str] = None
    favourites: Optional[int] = None
    anime_title_romaji: Optional[str] = None
    anime_title_english: Optional[str] = None


class StaffMediaMini(BaseModel):
    id: int
    title: Title
    coverImage: Optional[CoverImage] = None
    format: Optional[str] = None
    seasonYear: Optional[int] = None
    averageScore: Optional[int] = None


class StaffDetails(BaseModel):
    id: int
    name_full: str
    name_native: Optional[str] = None
    name_alternative: List[str] = Field(default_factory=list)
    image_large: Optional[str] = None
    description: Optional[str] = None
    primary_occupations: List[str] = Field(default_factory=list)
    gender: Optional[str] = None
    date_of_birth: Optional[DateOfBirth] = None
    date_of_death: Optional[DateOfBirth] = None
    age: Optional[int] = None
    years_active: List[int] = Field(default_factory=list)
    home_town: Optional[str] = None
    blood_type: Optional[str] = None
    favourites: Optional[int] = None
    works: List[StaffMediaMini] = Field(default_factory=list)
    works_total: int = 0
    works_has_next: bool = False


# ==============USERS==================
class Avatar(BaseModel):
    large: Optional[str] = None
    medium: Optional[str] = None


class AnimeStats(BaseModel):
    count: Optional[int] = None
    meanScore: Optional[float] = None
    minutesWatched: Optional[int] = None
    episodesWatched: Optional[int] = None


class MangaStats(BaseModel):
    count: Optional[int] = None
    meanScore: Optional[float] = None
    chaptersRead: Optional[int] = None
    volumesRead: Optional[int] = None


class UserStatistics(BaseModel):
    anime: Optional[AnimeStats] = None
    manga: Optional[MangaStats] = None


class TitleShort(BaseModel):
    userPreferred: Optional[str] = None
    romaji: Optional[str] = None
    english: Optional[str] = None


class MediaMini(BaseModel):
    id: int
    title: TitleShort
    coverImage: Optional[CoverImage] = None  


class NameFull(BaseModel):
    full: Optional[str] = None
    native: Optional[str] = None


class CharacterMini(BaseModel):
    id: int
    name: NameFull
    image: Optional[StaffImage] = None  


class UserFavourites(BaseModel):
    anime: List[MediaMini] = Field(default_factory=list)
    manga: List[MediaMini] = Field(default_factory=list)
    characters: List[CharacterMini] = Field(default_factory=list)
    staff: List[CharacterMini] = Field(default_factory=list)  


class UserProfile(BaseModel):
    id: int
    name: str
    avatar: Optional[Avatar] = None
    bannerImage: Optional[str] = None
    about: Optional[str] = None
    statistics: Optional[UserStatistics] = None
    favourites: Optional[UserFavourites] = None
    createdAt: Optional[int] = None  # unix timestamp
    updatedAt: Optional[int] = None
    siteUrl: Optional[str] = None
    donatorTier: Optional[int] = None
    moderatorRoles: Optional[List[str]] = None