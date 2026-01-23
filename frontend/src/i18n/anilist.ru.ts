/* ===================== SEASONS ===================== */
export const SEASONS: Record<string, string> = {
	WINTER: 'Зима',
	SPRING: 'Весна',
	SUMMER: 'Лето',
	FALL: 'Осень',
  }
  
  /* ===================== MEDIA FORMAT ===================== */
  export const FORMATS: Record<string, string> = {
	TV: 'ТВ-сериал',
	TV_SHORT: 'Короткий сериал',
	MOVIE: 'Фильм',
	SPECIAL: 'Спешл',
	OVA: 'OVA',
	ONA: 'ONA',
	MUSIC: 'Музыкальное видео',
	MANGA: 'Манга',
	NOVEL: 'Ранобэ',
	ONE_SHOT: 'Ваншот',
  }
  
  /* ===================== MEDIA STATUS ===================== */
  export const STATUS: Record<string, string> = {
	FINISHED: 'Завершено',
	RELEASING: 'Онгоинг',
	NOT_YET_RELEASED: 'Анонсировано',
	CANCELLED: 'Отменено',
	HIATUS: 'Приостановлено',
  }
  
  /* ===================== MEDIA TYPE ===================== */
  export const MEDIA_TYPE: Record<string, string> = {
	ANIME: 'Аниме',
	MANGA: 'Манга',
	NOVEL: 'Ранобэ',
  }
  
  /* ===================== CHARACTER ROLE ===================== */
  export const CHARACTER_ROLE: Record<string, string> = {
	MAIN: 'Главный',
	SUPPORTING: 'Второстепенный',
	BACKGROUND: 'Фоновый',
  }
  
  /* ===================== STAFF ROLE ===================== */
  export const STAFF_ROLE: Record<string, string> = {
	DIRECTOR: 'Режиссёр',
	ORIGINAL_CREATOR: 'Автор оригинала',
	CHARACTER_DESIGN: 'Дизайн персонажей',
	MUSIC: 'Музыка',
	SCRIPT: 'Сценарий',
  }
  
  /* ===================== GENRES ===================== */
  export const GENRES: Record<string, string> = {
	Action: 'Экшен',
	Adventure: 'Приключения',
	Comedy: 'Комедия',
	Drama: 'Драма',
	Ecchi: 'Этти',
	Fantasy: 'Фэнтези',
	Horror: 'Ужасы',
	MahouShoujo: 'Махо-сёдзё',
	Mecha: 'Меха',
	Music: 'Музыка',
	Mystery: 'Мистика',
	Psychological: 'Психология',
	Romance: 'Романтика',
	SciFi: 'Научная фантастика',
	SliceOfLife: 'Повседневность',
	Sports: 'Спорт',
	Supernatural: 'Сверхъестественное',
	Thriller: 'Триллер'
  }
  export const SOURCES = {
	ORIGINAL: 'Оригинал',
	MANGA: 'Манга',
	LIGHT_NOVEL: 'Ранобэ',
	VISUAL_NOVEL: 'Визуальная новелла',
	GAME: 'Игра',
	OTHER: 'Другое'
  } as const
  
  /* ===================== HELPERS ===================== */
  export const t = (
	dict: Record<string, string>,
	key?: string | null,
	fallback = '—'
  ) => {
	if (!key) return fallback
	return dict[key] ?? key
  }
  