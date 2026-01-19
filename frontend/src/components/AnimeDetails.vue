<script setup lang="ts">
  import { ref, computed, watch, onMounted, onUnmounted, reactive } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import RelationsRow from './RelationsTimeline.vue'
  import StaffTable from './StaffTable.vue'
  
  interface Trailer {
    id: string
    site: 'youtube' | 'dailymotion'
    thumbnail?: string
  }
  
  interface StreamingEpisode {
    title?: string
    thumbnail?: string
    site?: string
    url?: string
  }
  
  interface AnimeMedia {
    trailer?: Trailer | null
    streamingEpisodes?: StreamingEpisode[]
    // ... другие поля по необходимости
  }
  type ReviewType = 'all' | 'positive' | 'neutral' | 'negative'

  interface Review {
    id: number
    type: ReviewType
    text: string
  }

const reviews = ref<Review[]>([])
  const route = useRoute()
  const previewScreenshots = computed(() => {
    return screenshots.value.slice(0, 4)
  })

  const hasMoreScreenshots = computed(() => {
    return screenshots.value.length > 4
  })

  const anime = ref<any>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)
  type DiscussionTab = 'comments' | 'reviews'
  const activeDiscussionTab = ref<DiscussionTab>('comments')

  const setDiscussionTab = (tab: DiscussionTab) => {
    activeDiscussionTab.value = tab
  }
  
  const trailerUrl = computed(() => {
    const t = anime.value?.trailer
    if (!t || t.site !== 'youtube') return null
    return `https://www.youtube.com/embed/${t.id}`
  })
  
  const screenshots = computed(() => {
    return (
      anime.value?.streamingEpisodes
        ?.map((e: StreamingEpisode) => e.thumbnail)
        .filter(Boolean) ?? []
    )
  })
  const ratings = computed(() => ({
    anilist: anime.value?.averageScore
      ? (anime.value.averageScore / 10).toFixed(1)
      : null,

    kinopoisk: null,
    shikimori: null,
  }))


  /* Модальные окна */
  const isPosterOpen = ref(false)
  const activeScreenshot = ref<string | null>(null)
  
  /* Статус просмотра */
  type Status = 'watching' | 'planned' | 'completed' | 'paused' | 'dropped' | null
  const userStatus = ref<Status>(null)
  const menuOpen = ref(false)
  
  /* Язык описания */
  const descriptionLang = ref<'ru' | 'en'>('ru')
  
  const descriptionRu = computed(() => anime.value?.descriptionRu ?? null)
  const descriptionEn = computed(() => anime.value?.description ?? null)
  
  const activeDescription = computed(() => {
    if (descriptionLang.value === 'ru' && descriptionRu.value) {
      return descriptionRu.value
    }
    return descriptionEn.value || 'Описание отсутствует'
  })
  
  /* Персонажи */
  const characters = computed(() => {
    if (!anime.value?.characters?.edges) return []

    return anime.value.characters.edges.filter(
      (c: any) => c.role === 'MAIN' || c.role === 'SUPPORTING'
    )
  })

  const previewCharacters = computed(() => characters.value.slice(0, 6))

  
  /* Методы */
  const openPoster = () => {
    isPosterOpen.value = true
    document.body.style.overflow = 'hidden'
  }
  
  const closePoster = () => {
    isPosterOpen.value = false
    document.body.style.overflow = ''
  }
  
  const openScreenshot = (src: string) => {
    activeScreenshot.value = src
    document.body.style.overflow = 'hidden'
  }
  
  const closeScreenshot = () => {
    activeScreenshot.value = null
    document.body.style.overflow = ''
  }
  
  const toggleMenu = () => {
    menuOpen.value = !menuOpen.value
  }
  
  const setStatus = (status: Status) => {
    userStatus.value = status
    menuOpen.value = false
  }
  
  const toggleDescriptionLang = () => {
    descriptionLang.value = descriptionLang.value === 'ru' ? 'en' : 'ru'
  }
  
  const userStatusLabel = (status: Status) => {
    switch (status) {
      case 'watching':   return 'Смотрю'
      case 'planned':    return 'В планах'
      case 'completed':  return 'Просмотрено'
      case 'paused':     return 'Отложено'
      case 'dropped':    return 'Заброшено'
      default:           return 'Выбрать статус'
    }
  }
  
  /* Закрытие по Escape */
  const onKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      if (isPosterOpen.value) closePoster()
      if (activeScreenshot.value) closeScreenshot()
    }
  }
  
  /* Закрытие выпадающего меню при клике вне */
  const onClickOutside = (e: MouseEvent) => {
    const target = e.target as HTMLElement
    if (!target.closest('.status-dropdown')) {
      menuOpen.value = false
    }
  }
  
  /* Загрузка данных */
  const loadAnime = async (id: number) => {
    loading.value = true
    error.value = null
  
    try {
      const res = await fetch(`http://127.0.0.1:8000/anime/${id}`)
      if (!res.ok) throw new Error('Не удалось загрузить данные')
      anime.value = await res.json()
    } catch (err) {
      console.error(err)
      error.value = 'Ошибка загрузки данных аниме'
    } finally {
      loading.value = false
    }
  }
  
    const activeReviewFilter = ref<ReviewType>('all')

      const reviewCounters = computed(() => ({
          all: reviews.value.length,
          positive: reviews.value.filter(r => r.type === 'positive').length,
          neutral: reviews.value.filter(r => r.type === 'neutral').length,
          negative: reviews.value.filter(r => r.type === 'negative').length,
        }))


    const setReviewFilter = (type: ReviewType) => {
      activeReviewFilter.value = type
    }
  
  watch(
    () => route.params.id,
    (newId) => {
      const id = Number(newId)
      if (!Number.isNaN(id)) {
        loadAnime(id)
      }
    },
    { immediate: true }
  )
  
  onMounted(() => {
    window.addEventListener('keydown', onKeyDown)
    document.addEventListener('click', onClickOutside)
  })
  
  onUnmounted(() => {
    window.removeEventListener('keydown', onKeyDown)
    document.removeEventListener('click', onClickOutside)
  })
  </script>
  
  <template>
    <div class="anime-detail">
      <div v-if="loading" class="loading">Загрузка...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
  
      <template v-else-if="anime">
        <!-- BANNER -->
        <div
          class="banner"
          :style="{ backgroundImage: `url(${anime.bannerImage || anime.coverImage?.large || ''})` }"
        />
  
        <!-- Основная информация -->
        <div class="main-info-v2">
          <!-- Постер + статус -->
          <div class="poster-wrap">
            <img
              :src="anime.coverImage?.extraLarge"
              class="poster"
              alt="Poster"
              @click="openPoster"
            />
  
            <!-- Выбор статуса просмотра -->
            <div class="watch-status status-dropdown">
              <button
                class="status-btn"
                :class="userStatus"
                @click.stop="toggleMenu"
              >
                {{ userStatusLabel(userStatus) }}
              </button>
  
              <div v-if="menuOpen" class="status-menu">
                <button @click="setStatus('watching')">Смотрю</button>
                <button @click="setStatus('planned')">В планах</button>
                <button @click="setStatus('completed')">Просмотрено</button>
                <button @click="setStatus('paused')">Отложено</button>
                <button @click="setStatus('dropped')">Заброшено</button>
                <button @click="setStatus(null)">Убрать статус</button>
              </div>
            </div>
          </div>
  
          <!-- Контент -->
          <div class="content-wrap">
            <div class="title-row">
              <h2>{{ anime.title?.romaji || 'Без названия' }}</h2>
            </div>
  
            <p v-if="anime.title?.english" class="alt-title">
              {{ anime.title.english }}
            </p>
  
            <div class="meta-strip">
              <span>{{ anime.format || '?' }}</span>
              <span>{{ anime.status || '?' }}</span>
              <span>~{{ anime.episodes || '?' }} эп.</span>
            </div>
            <div class="rating-sources">
            <!-- AniList -->
            <div class="rating-badge anilist" v-if="ratings.anilist">
              <span class="source">AniList</span>
              <span class="value">{{ ratings.anilist }}</span>
            </div>

            <!-- Kinopoisk -->
            <div class="rating-badge kinopoisk disabled">
              <span class="source">КиноПоиск</span>
              <span class="value">—</span>
            </div>

            <!-- Shikimori -->
            <div class="rating-badge shikimori disabled">
              <span class="source">Shikimori</span>
              <span class="value">—</span>
            </div>
          </div>

  
            <div class="meta-secondary">
              <span>{{ anime.season }} / {{ anime.seasonYear || '?' }}</span>
            </div>
  
            <div class="actions-row">
              <button title="В избранное"><span class="material-symbols-outlined">bookmark</span></button>
              <button title="Комментарий"><span class="material-symbols-outlined">comment</span></button>
              <button title="Отзыв"><span class="material-symbols-outlined">rate_review</span></button>
              <button title="В плейлист"><span class="material-symbols-outlined">playlist_add</span></button>
              <button title="Поделиться"><span class="material-symbols-outlined">share</span></button>
              <button title="Смотреть"><span class="material-symbols-outlined">play_circle</span></button>
            </div>
  
            <div class="genres" v-if="anime.genres?.length">
              <strong>Жанры:</strong>
              <div class="genre-list">
                <span v-for="genre in anime.genres" :key="genre" class="genre">
                  {{ genre }}
                </span>
              </div>
            </div>
  
            <div class="footer-info">
              <div class="studios" v-if="anime.studios?.nodes?.length">
                <h2>Студия:</h2>
                <h3>{{ anime.studios.nodes.map((s: any) => s.name).join(', ') }}</h3>
              </div>
            </div>
          </div>
        </div>
  
        <!-- Описание -->
        <div class="description-wrapper">
          <div class="description-header">
            <h2>Описание</h2>
  
            <button
              class="lang-toggle"
              :disabled="!descriptionRu"
              @click="toggleDescriptionLang"
              :title="descriptionLang === 'ru' ? 'Показать на английском' : 'Показать на русском'"
            >
              <span class="material-symbols-outlined">
                {{ descriptionLang === 'ru' ? 'translate' : 'language' }}
              </span>
              <span class="lang-label">{{ descriptionLang.toUpperCase() }}</span>
            </button>
          </div>
  
          <div class="description" v-html="activeDescription" />
        </div>
  
        <!-- Связи и персонал -->
        <div class="relations-layout">
          <RelationsRow v-if="anime.relations?.edges?.length" :relations="anime.relations" />
  
          <StaffTable v-if="anime?.staff?.edges?.length" :staff="anime.staff" :limit="10" />
        </div>
  
        <!-- Персонажи -->
        <section class="characters" v-if="characters.length">
          <h2>Персонажи</h2>
  
          <div class="char-grid">
            <router-link
              v-for="edge in previewCharacters"
              :key="edge.node.id"
              :to="`/character/${edge.node.id}`"
              class="char-card"
            >
              <img :src="edge.node.image?.large" alt="" />
              <p class="char-name">{{ edge.node.name?.full || '???' }}</p>
            </router-link>
  
            <router-link
              :to="`/anime/${route.params.id}/characters`"
              class="char-card show-all"
            >
              <span class="material-symbols-outlined">group</span>
              <p>Все персонажи</p>
            </router-link>
          </div>
        </section>
  
        <!-- Скриншоты -->
        <section v-if="screenshots.length" class="media-section">
          <h2>Скриншоты</h2>
          <div class="screenshots-grid">
            <img
              v-for="(img, i) in previewScreenshots"
              :key="i"
              :src="img"
              class="screenshot"
              @click="openScreenshot(img)"
            />

            <!-- КНОПКА "ВСЕ СКРИНШОТЫ" -->
            <router-link
              v-if="hasMoreScreenshots"
              :to="`/anime/${route.params.id}/screenshots`"
              class="screenshot show-all-screens"
            >
              <span class="material-symbols-outlined">collections</span>
              <span>Все скриншоты</span>
            </router-link>
          </div>
        </section>
  
        <!-- Трейлер -->
        <section v-if="trailerUrl" class="media-section">
          <h2>Трейлер</h2>
          <div class="trailer-wrap">
            <iframe :src="trailerUrl" title="Trailer" allowfullscreen />
          </div>
        </section>
        <section class="discussion-section">
        <div class="discussion-header">
          <h2>Обсуждение</h2>

          <div class="discussion-tabs">
            <button
              :class="{ active: activeDiscussionTab === 'comments' }"
              @click="setDiscussionTab('comments')"
            >
              Комментарии
            </button>

            <button
              :class="{ active: activeDiscussionTab === 'reviews' }"
              @click="setDiscussionTab('reviews')"
            >
              Рецензии
            </button>
          </div>
        </div>

        <!-- КОММЕНТАРИИ -->
        <div v-if="activeDiscussionTab === 'comments'" class="discussion-body">
          <div class="empty-state">
            <span class="material-symbols-outlined">chat</span>
            <p>Комментариев пока нет</p>
            <button class="primary-btn">Написать комментарий</button>
          </div>
        </div>

        <!-- РЕЦЕНЗИИ -->
        <div v-else class="discussion-body">
          <div class="reviews-filter-bar">
        <button
          class="filter-pill"
          :class="{ active: activeReviewFilter === 'all' }"
          @click="setReviewFilter('all')"
        >
          Все отзывы ({{ reviewCounters.all }})
        </button>

        <button
          class="filter-pill positive"
          :class="{ active: activeReviewFilter === 'positive' }"
          :disabled="reviewCounters.positive === 0"
          @click="setReviewFilter('positive')"
        >
          <span class="material-symbols-outlined">sentiment_satisfied</span>
          Положительные ({{ reviewCounters.positive }})
        </button>

        <button
          class="filter-pill neutral"
          :class="{ active: activeReviewFilter === 'neutral' }"
          @click="setReviewFilter('neutral')"
        >
          <span class="material-symbols-outlined">sentiment_neutral</span>
          Нейтральные ({{ reviewCounters.neutral }})
        </button>

        <button
          class="filter-pill negative"
          :class="{ active: activeReviewFilter === 'negative' }"
          @click="setReviewFilter('negative')"
        >
          <span class="material-symbols-outlined">sentiment_dissatisfied</span>
          Отрицательные ({{ reviewCounters.negative }})
        </button>
      </div>

      <!-- КОНТЕНТ -->
      <div class="reviews-content">
        <p class="stub">
          Активный фильтр: <strong>{{ activeReviewFilter }}</strong>
        </p>
      </div>

        </div>
      </section>

        <!-- Модалка полноэкранного постера -->
        <div v-if="isPosterOpen" class="poster-overlay" @click.self="closePoster">
          <img
            :src="anime.coverImage?.extraLarge"
            class="poster-full"
            alt="Full size poster"
            @click="closePoster"
          />
        </div>
  
        <!-- Модалка скриншота -->
        <div
          v-if="activeScreenshot"
          class="media-overlay"
          @click.self="closeScreenshot"
        >
          <img
            :src="activeScreenshot"
            class="media-full"
            alt="Full screenshot"
            @click="closeScreenshot"
          />
        </div>
      </template>
    </div>
  </template>
  
  <style scoped>
  .anime-detail {

    min-height: 100vh;
    color: #e6e6eb;
  }
  
  /* BANNER */
  .banner {
    height: 320px;
    background-size: cover;
    background-position: center;
  }
  
  /* MAIN */
  .main-info {
    max-width: 1400px;
    margin: -140px auto 0;
    padding: 0 32px;
    display: grid;
    grid-template-columns: 300px 1fr;
    gap: 48px;
  }
  
  /* POSTER COLUMN */
  .poster-column {
    display: flex;
    flex-direction: column;
    gap: 14px;
  }
  
  /* COVER */
  .cover {
    width: 100%;
    border-radius: 18px;
    box-shadow: 0 30px 80px rgba(0,0,0,0.8);
  }
  
  .clickable {
    cursor: zoom-in;
  }
  
  /* ACTIONS */
  .poster-actions {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
  }
  
  .action-btn {
    display: flex;
    align-items: center;
    padding: 10px 14px;
    border-radius: 12px;
    font-size: 0.85rem;
    background: rgba(255,255,255,0.06);
    color: #dfe2ff;
    border: none;
    cursor: pointer;
  }
  
  .action-btn.active {
    background: var(--accent-primary);
  }
  
  .fav-btn {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: rgba(255,255,255,0.06);
    color: #ffd166;
    border: none;
  }
  
  /* DETAILS */
  .details {
    position: relative;
    backdrop-filter: blur(34px);
    border-radius: 24px;
    padding: 32px;
  }
  
  /* TAGS */
  .tags {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
  }
  
  .tag {
    padding: 6px 14px;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
  }
  
  .score {
    font-weight: 700;
    border: 2px solid #a3e635;
  }
  
  /* CHARACTERS */
  .characters {
  max-width: 1480px;
  margin: 80px auto;
  padding: 0 32px;
}

.char-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 20px;
}

/* КАРТОЧКА */
.char-card {
  height: 277.7px;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
  transition: transform .2s ease, box-shadow .2s ease;
}

.char-card img {
  width: 100%;
  aspect-ratio: 2 / 3;
  object-fit: cover;
  border-radius: 14px;
  box-shadow: 0 12px 30px rgba(0,0,0,.45);
}

.char-card:hover {
  transform: translateY(-6px);
}

/* ИМЯ */
.char-name {
  margin-top: 10px;
  font-size: .95rem;
  text-align: center;
  opacity: .9;
}

/* ПОКАЗАТЬ ВСЕХ */
.show-all {
  
  justify-content: center;
  align-items: center;
  background: rgba(255,255,255,.04);
  border-radius: 14px;
  min-height: 250px;
  border: 1px dashed rgba(255,255,255,.15);
}

.show-all span {
  font-size: 46px;
  opacity: .7;
  margin-bottom: 8px;
}

.show-all p {
  font-size: .9rem;
  opacity: .8;
}


.hero-content {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 48px;
  align-items: start;
}

.hero-poster img {
  border-radius: 18px;
  box-shadow: 0 30px 80px rgba(0,0,0,0.85);
}

.hero-info {
  backdrop-filter: blur(30px);
  background: rgba(20, 22, 40, 0.6);
  border-radius: 28px;
  padding: 32px;
}

.hero-actions {
  display: flex;
  gap: 12px;
  margin: 18px 0;
}
.action-bar {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.icon-btn {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(255,255,255,0.06);
  border: none;
  color: #dfe2ff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: 
    background 0.2s ease,
    transform 0.15s ease;
}

.icon-btn:hover {
  background: rgba(255,255,255,0.12);
  transform: translateY(-2px);
}

.icon-btn.active {
  background: var(--accent-primary);
  color: #ffd166;
}

.icon-btn span {
  font-size: 22px;
}
.main-info-v2 {
  max-width: 1360px;
  margin: -100px auto 0;
  padding: 32px;
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 48px;
  background: rgba(15, 18, 32, 0.6);
  backdrop-filter: blur(30px);
  border-radius: 28px;
}

/* POSTER */
.poster-wrap {
  position: relative;
}
.poster {
  width: 100%;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0,0,0,.6);
  cursor: zoom-in;
  position: relative;
  z-index: 1;
}

/* CONTENT */
.title-row {
  display: flex;
  align-items: baseline;
  gap: 14px;
}
.title-row h1 {
  font-size: 2.1rem;
  font-weight: 600;
  letter-spacing: .2px;
}

.year {
  font-size: .95rem;
  opacity: .5;
}


.alt-title {
  margin-top: 4px;
  opacity: 0.6;
}

/* META */

.meta-strip {
  display: flex;
  gap: 14px;
  margin: 20px 0;
  font-size: .85rem;
}

.meta-strip span {
  padding: 6px 14px;
  background: rgba(255,255,255,.05);
  border-radius: 10px;
}
.meta-secondary {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  
  padding: 4px 10px;
  border-radius: 8px;
  margin-bottom: 1.2em;
  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: 0.02em;

  background: rgba(255, 255, 255, 0.06);
  color: #e5e7eb;

  border: 1px solid rgba(255, 255, 255, 0.12);
}
.watch-status {
  position: relative;
  margin-bottom: 20px;
  margin-top: 15px;
}

.status-btn {
  position: relative;
  width: 100%;
  padding: 10px 18px;
  border-radius: 5px;
  background-color: transparent;
  border: 1px solid var(--bg-tertiary);
  border: none;
  cursor: pointer;
  font-size: .9rem;
  z-index: 3;
}

.status-menu {
  position: absolute;
  width: 100%;
  background: rgba(20, 22, 40, 0.96);
  backdrop-filter: blur(12px);
  padding: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  z-index: 10;
}

.status-menu button {
  width: 100%;
  background: transparent;
  border: none;
  padding: 8px 14px;
  text-align: left;
}

.status-menu button:hover {
  background: rgba(255,255,255,.08);
  filter: brightness(1.1);
  transform: translateY(-1px);
}


/* ACTIONS */
.actions-row {
  display: flex;
  gap: 12px;
  margin-bottom: 26px;
}

.actions-row button {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.06);
}
/* СМОТРЮ */
.status-btn.watching {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  box-shadow: 0 0 0 1px rgba(34,197,94,.35);
}

/* В ПЛАНАХ */
.status-btn.planned {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  box-shadow: 0 0 0 1px rgba(59,130,246,.35);
}

/* ПРОСМОТРЕНО */
.status-btn.completed {
  background: linear-gradient(135deg, #a855f7, #7c3aed);
  box-shadow: 0 0 0 1px rgba(168,85,247,.35);
}

/* ОТЛОЖЕНО */
.status-btn.paused {
  background: linear-gradient(135deg, #f59e0b, #d97706);
  box-shadow: 0 0 0 1px rgba(245,158,11,.35);
}

/* ЗАБРОШЕНО */
.status-btn.dropped {
  background: linear-gradient(135deg, #ef4444, #dc2626);
  box-shadow: 0 0 0 1px rgba(239,68,68,.35);
}

/* БЕЗ СТАТУСА */
.status-btn:not(.watching):not(.planned):not(.completed):not(.paused):not(.dropped) {
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.12);
}
.actions-row button:hover {
  background: rgba(255,255,255,.1);
}
.description-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.lang-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 999px;
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.1);
  color: #cfd2ff;
  cursor: pointer;
  font-size: .8rem;
}

.lang-toggle:hover:not(:disabled) {
  background: rgba(255,255,255,.12);
}

.lang-toggle:disabled {
  opacity: .4;
  cursor: not-allowed;
}

.lang-label {
  font-weight: 500;
  letter-spacing: .5px;
}

.description-wrapper{
  width: 1200px;
  margin: 4em auto;

}
/* DESCRIPTION */
.description {
  margin-top: 8px;
  line-height: 1.75;
  color: #d8d9e6;
}


/* FOOTER */
.footer-info {
  margin-top: 26px;
  font-size: .85rem;
  color: #9ca3af;
}
.details {
  position: relative; /* ОБЯЗАТЕЛЬНО */
}

/* студия в углу */
.studios {
  position: absolute;
  top: 32px;
  right: 32px;
  font-size: 1.75rem;
  color: #aab0ff;
  opacity: 0.85;
  border-radius: 15px;
  padding: 12px 24px;
}
.genres {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  margin: 14px 0 18px;
}

.genre-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.genre {
  font-size: 1.02rem;
  padding: 5px 12px;
  border-radius: 999px;
  color: #c7c9ff;
  letter-spacing: 0.3px;
  text-transform: uppercase;

  border: 1px solid rgba(255,255,255,0.08);
}
.relations-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: start;
  gap: 32px;
  max-width: 1780px;
  margin: 60px auto;
  padding: 0 32px;
}
.media-section {
  max-width: 1480px;
  margin: 80px auto;
  padding: 0 32px;
}

.screenshots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 18px;
}

.screenshot {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  border-radius: 14px;
  cursor: zoom-in;
  transition: transform .2s ease, box-shadow .2s ease;
}

.screenshot:hover {
  transform: scale(1.03);
  box-shadow: 0 20px 50px rgba(0,0,0,.5);
}
.media-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.media-full {
  max-width: 90%;
  max-height: 90%;
  border-radius: 18px;
}
.trailer-wrap {
  position: relative;
  border-radius: 18px;
  margin-bottom: 10.5em;
}

.trailer-wrap iframe {
  position: absolute;
  inset: 0;
}
.show-all-screens {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;

  background: rgba(255,255,255,.05);
  border: 1px dashed rgba(255,255,255,.2);
  border-radius: 14px;

  color: #cfd2ff;
  text-decoration: none;
  cursor: pointer;

  transition: background .2s ease, transform .2s ease;
}

.show-all-screens:hover {
  background: rgba(255,255,255,.1);
  transform: scale(1.03);
}

.show-all-screens span:first-child {
  font-size: 42px;
  opacity: .8;
}
/* DISCUSSION */
.discussion-section {
  max-width: 1480px;
  margin: 80px auto;
  padding: 0 32px;
}

.discussion-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.discussion-header h2 {
  font-size: 1.4rem;
  font-weight: 600;
}

.discussion-tabs {
  display: flex;
  gap: 10px;
}

.discussion-tabs button {
  padding: 8px 18px;
  border-radius: 10px;
  background: rgba(255,255,255,.06);
  border: 1px solid rgba(255,255,255,.1);
  color: #cfd2ff;
  cursor: pointer;
  font-size: .85rem;
  transition: all .2s ease;
}

.discussion-tabs button.active {
  color: white;
  border-color: transparent;
}

.discussion-tabs button:hover {
  background: rgba(255,255,255,.12);
}

/* BODY */
.discussion-body {
  background: rgba(20, 22, 40, 0.6);
  border-radius: 24px;
  padding: 48px;
  margin-top: 3em;
  backdrop-filter: blur(18px);
}

/* EMPTY STATE */
.empty-state {
  text-align: center;
  color: #9ca3af;
}

.empty-state span {
  font-size: 48px;
  opacity: .6;
  margin-bottom: 10px;
  display: block;
}

.empty-state p {
  margin-bottom: 16px;
  font-size: .95rem;
}

/* BUTTON */
.primary-btn {
  padding: 10px 20px;
  border-radius: 999px;
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
  border: none;
  cursor: pointer;
  font-size: .85rem;
}

.primary-btn:hover {
  filter: brightness(1.1);
}
/* FILTER BAR */
.reviews-filter-bar {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}

/* PILL */
.filter-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 999px;
  background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.1);
  color: #cfd2ff;
  font-size: .85rem;
  cursor: pointer;
  transition: all .2s ease;
}

.filter-pill span {
  font-size: 18px;
  opacity: .8;
}

/* ACTIVE */
.filter-pill.active {
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  border-color: transparent;
  color: white;
}

/* TYPES */
.filter-pill.positive {
  color: #86efac;
}
.filter-pill.neutral {
  color: #fde68a;
}
.filter-pill.negative {
  color: #fca5a5;
}

/* HOVER */
.filter-pill:hover {
  background: rgba(255,255,255,.1);
}

/* CONTENT */
.reviews-content {
  background: rgba(20,22,40,.6);
  border-radius: 20px;
  padding: 32px;
}

.stub {
  opacity: .6;
}
.rating-sources {
  display: flex;
  gap: 12px;
  margin-top: 12px;
  flex-wrap: wrap;
  margin-bottom: 1em;
}

.rating-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  
  padding: 4px 10px;
  border-radius: 8px;

  font-size: 0.78rem;
  font-weight: 500;
  letter-spacing: 0.02em;

  background: rgba(255, 255, 255, 0.06);
  color: #e5e7eb;

  border: 1px solid rgba(255, 255, 255, 0.12);
}

.rating-badge .source {
  opacity: 0.6;
  font-weight: 400;
}

.rating-badge .value {
  font-weight: 600;
  font-size: 0.82rem;
}

/* AniList */
.rating-badge.anilist {
  border-color: rgba(59, 130, 246, 0.45);
  color: #93c5fd;
}

/* Kinopoisk */
.rating-badge.kinopoisk {
  border-color: rgba(245, 158, 11, 0.45);
  color: #facc15;
}

/* Shikimori */
.rating-badge.shikimori {
  border-color: rgba(239, 68, 68, 0.45);
  color: #fca5a5;
}

/* Заглушка */
.rating-badge.disabled {
  opacity: 0.35;
  border-style: dashed;
}

  </style>
  