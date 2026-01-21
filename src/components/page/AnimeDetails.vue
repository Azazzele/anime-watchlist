<script setup lang="ts">
  import { ref, watch, onMounted, onUnmounted } from 'vue'
  
  import AnimeBanner from '../ui/anime/AnimeBanner.vue'
  import AnimePosterWithStatus from '../ui/anime/AnimePosterWithStatus.vue'
  import AnimeMainInfo from '../ui/anime/AnimeMainInfo.vue'
  import AnimeDescription from '../ui/anime/AnimeDescription.vue'
  import AnimeRelationsAndStaff from '../ui/anime/AnimeRelationsAndStaff.vue'
  import AnimeCharactersPreview from '../ui/anime/AnimeCharactersPreview.vue'
  import AnimeScreenshotsGrid from '../ui/anime/AnimeScreenshotsGrid.vue'
  import AnimeTrailer from '../ui/anime/AnimeTrailer.vue'
  import AnimeDiscussion from '../ui/anime/AnimeDiscussion.vue'
  
  import PosterModal from '../ui/anime/modals/PosterModal.vue'
  import ScreenshotModal from '../ui/anime/modals/ScreenshotModal.vue'
  
  import type { Media } from '../../types/type'
  
  /* ===================== PROPS ===================== */
  const props = defineProps<{
    id: number
    type: 'anime' | 'manga' | 'ranobe'
  }>()
  
  /* ===================== STATE ===================== */
  const media = ref<Media | null>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)
  
  /* ===================== TYPE MAP ===================== */
  const mediaTypeMap = {
    anime: 'ANIME',
    manga: 'MANGA',
    ranobe: 'NOVEL'
  } as const
  
  /* ===================== LOAD MEDIA ===================== */
  const loadMedia = async () => {
    loading.value = true
    error.value = null

    try {
      const res = await fetch(
        `http://127.0.0.1:8000/anime/${props.id}`
      )
      if (!res.ok) throw new Error('Ошибка загрузки')

      const data = await res.json()
      media.value = data 
    } catch (e) {
      error.value = 'Не удалось загрузить данные'
    } finally {
      loading.value = false
    }
  }


  
  watch(
    () => [props.id, props.type],
    loadMedia,
    { immediate: true }
  )
  
  /* ===================== MODALS ===================== */
  const posterOpen = ref(false)
  const activeScreenshot = ref<string | null>(null)
  
  const openPoster = () => {
    posterOpen.value = true
    document.body.style.overflow = 'hidden'
  }
  const closePoster = () => {
    posterOpen.value = false
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
  
  /* ===================== ESC HANDLER ===================== */
  const onKeydown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      if (posterOpen.value) closePoster()
      if (activeScreenshot.value) closeScreenshot()
    }
  }
  
  onMounted(() => {
    window.addEventListener('keydown', onKeydown)
  })
  
  onUnmounted(() => {
    window.removeEventListener('keydown', onKeydown)
  })
  </script>
  
  <template>
    <div class="anime-detail">
      <div v-if="loading" class="loading">Загрузка...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
  
      <template v-else-if="media">
        <!-- Banner -->
        <AnimeBanner
          :background="media.bannerImage || media.coverImage?.large"
        />
  
        <!-- Main info -->
        <div class="main-info-v2">
          <AnimePosterWithStatus
            :cover="media.coverImage?.extraLarge"
            @open-poster="openPoster"
          />
  
          <AnimeMainInfo :anime="media" />
        </div>
  
        <!-- Description -->
        <AnimeDescription :anime="media" />
  
        <!-- Relations & Staff -->
        <AnimeRelationsAndStaff :anime="media" />
  
        <!-- Characters (только если есть) -->
        <AnimeCharactersPreview
          v-if="media.characters?.edges?.length"
          :characters="media.characters.edges"
          :anime-id="media.id"
        />
  
        <!-- Screenshots (ТОЛЬКО ДЛЯ ANIME) -->
        <AnimeScreenshotsGrid
          v-if="media.type === 'ANIME'"
          :thumbnails="
            media.streamingEpisodes
              ?.map(e => e.thumbnail)
              .filter((t): t is string => !!t) ?? []
          "
          :anime-id="props.id"
          @open="openScreenshot"
        />
  
        <!-- Trailer (ТОЛЬКО ДЛЯ ANIME) -->
        <AnimeTrailer
          v-if="media.type === 'ANIME'"
          :trailer="media.trailer"
        />
  
        <AnimeDiscussion />
  
        <!-- Modals -->
        <PosterModal
          v-if="posterOpen"
          :src="media.coverImage?.extraLarge"
          @close="closePoster"
        />
  
        <ScreenshotModal
          v-if="activeScreenshot"
          :src="activeScreenshot"
          @close="closeScreenshot"
        />
      </template>
    </div>
  </template>
  
  <style scoped>
  .anime-detail {
    min-height: 100vh;
    color: #e6e6eb;
  }
  
  .loading,
  .error {
    text-align: center;
    padding: 120px 20px;
    font-size: 1.4rem;
    color: #94a3b8;
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
  </style>
  