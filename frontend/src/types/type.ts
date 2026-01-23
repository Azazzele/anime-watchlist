/* ===================== BASE ===================== */

export type MediaType = 'ANIME' | 'MANGA' | 'NOVEL'

export interface Title {
  romaji?: string
  english?: string
  native?: string
}

export interface FuzzyDate {
  year?: number
  month?: number
  day?: number
}

/* ===================== IMAGES ===================== */

export interface CoverImage {
  extraLarge?: string
  large?: string
  medium?: string
  color?: string
}

export interface CharacterImage {
  large?: string
  medium?: string
}

/* ===================== CHARACTERS ===================== */

export interface Character {
  id: number
  name?: {
    full?: string
    native?: string
  }
  image?: CharacterImage
}

export interface CharacterEdge {
  role: string // ❗ ОБЯЗАТЕЛЬНО string
  node: Character
}

export interface CharactersConnection {
  edges: CharacterEdge[]
}

/* ===================== STUDIOS ===================== */

export interface Studio {
  name: string
}

export interface StudiosConnection {
  nodes: Studio[]
}

/* ===================== STREAMING ===================== */

export interface StreamingEpisode {
  title?: string
  thumbnail?: string
  url?: string
}

/* ===================== TRAILER ===================== */

export interface Trailer {
  id?: string
  site?: 'youtube' | 'dailymotion'
  thumbnail?: string
}

/* ===================== MEDIA (BASE) ===================== */

export interface Media {
  id: number
  type: MediaType

  title?: Title

  format?: string
  status?: string
  season?: string
  seasonYear?: number

  episodes?: number
  duration?: number

  volumes?: number
  chapters?: number

  genres?: string[]

  averageScore?: number
  popularity?: number
  favourites?: number

  source?: string
  isAdult?: boolean

  startDate?: FuzzyDate

  studios?: StudiosConnection
}

/* ===================== ANIME ONLY ===================== */

export interface AnimeMedia extends Media {
  type: 'ANIME'

  bannerImage?: string
  coverImage?: CoverImage

  trailer?: Trailer
  streamingEpisodes?: StreamingEpisode[]

  characters?: CharactersConnection
}
