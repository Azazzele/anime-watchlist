export interface Avatar {
	large?: string
	medium?: string
  }
  
  export interface AnimeStats {
	count?: number
	meanScore?: number
	minutesWatched?: number
	episodesWatched?: number
  }
  
  export interface MangaStats {
	count?: number
	meanScore?: number
	chaptersRead?: number
	volumesRead?: number
  }
  
  export interface UserStatistics {
	anime?: AnimeStats
	manga?: MangaStats
  }
  
  export interface TitleShort {
	userPreferred?: string
	romaji?: string
	english?: string
  }
  
  export interface CoverImage {
	large?: string
  }
  
  export interface MediaMini {
	id: number
	title: TitleShort
	coverImage?: CoverImage
  }
  
  export interface NameFull {
	full?: string
	native?: string
  }
  
  export interface ImageLarge {
	large?: string
  }
  
  export interface CharacterMini {
	id: number
	name: NameFull
	image?: ImageLarge
  }
  
  export interface UserFavourites {
	anime: MediaMini[]
	manga: MediaMini[]
	characters: CharacterMini[]
	staff: CharacterMini[]
  }
  
  export interface UserProfile {
	id: number
	name: string
	avatar?: Avatar
	bannerImage?: string
	about?: string
	statistics?: UserStatistics
	favourites?: UserFavourites
	createdAt?: number
	updatedAt?: number
	siteUrl?: string
	donatorTier?: number
	moderatorRoles?: string[]
  }