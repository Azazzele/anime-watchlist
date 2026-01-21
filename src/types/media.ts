export interface RelationEdge {
	relationType: string
	node: {
	  id: number
	  title?: {
		romaji?: string
		english?: string
	  }
	  format?: string
	  startDate?: {
		year?: number
	  }
	  coverImage?: {
		large?: string
	  }
	}
  }