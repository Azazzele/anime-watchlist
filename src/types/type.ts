export interface Media {
	id: number
	type: 'ANIME' | 'MANGA' | 'NOVEL'
	title?: {
	  romaji?: string
	  english?: string
	  native?: string
	}
	bannerImage?: string
	coverImage?: {	
	  extraLarge?: string
	  large?: string
	}
	format?: string
	status?: string
	episodes?: number
	chapters?: number
	volumes?: number
	season?: string
	seasonYear?: number
	genres?: string[]
	studios?: {
	  nodes?: Array<{ name: string }>
	}
	averageScore?: number
	description?: string
	descriptionRu?: string
	trailer?: {
	  id?: string
	  site?: string
	}
	streamingEpisodes?: Array<{ thumbnail?: string }>
	characters?: {
	  edges?: Array<{
		role: 'MAIN' | 'SUPPORTING' | string
		node: {
		  id: number
		  name?: { full?: string }
		  image?: { large?: string }
		}
	  }>
	}
	relations?: any
	staff?: any
  }
  