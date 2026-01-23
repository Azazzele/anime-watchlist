<script setup lang="ts">
  import { ref, watch, onMounted, onUnmounted, computed } from 'vue'
  
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
  
  import type { Media, AnimeMedia } from '../../types/type'
  
  /* ===================== PROPS ===================== */
  const props = defineProps<{
    id: number
    type: 'anime' | 'manga' | 'ranobe'
  }>()
  
  /* ===================== STATE ===================== */
  const media = ref<Media | null>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)
  
  /* ===== ONLY ANIME MEDIA ===== */
  const anime = computed<AnimeMedia | null>(() => {
    return media.value?.type === 'ANIME'
      ? (media.value as AnimeMedia)
      : null
  })

  /* ===================== LOAD MEDIA ===================== */
  const loadMedia = async () => {
    loading.value = true
    error.value = null
  
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/media/${props.type}/${props.id}`
      )
      if (!res.ok) throw new Error()
  
      media.value = await res.json()
    } catch {
      error.value = 'Не удалось загрузить данные'
    } finally {
      loading.value = false
    }
  }
  
  watch(() => [props.id, props.type], loadMedia, { immediate: true })
  
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
  
  /* ===================== ESC ===================== */
  const onKeydown = (e: KeyboardEvent) => {
    if (e.key === 'Escape') {
      if (posterOpen.value) closePoster()
      if (activeScreenshot.value) closeScreenshot()
    }
  }
  
  onMounted(() => window.addEventListener('keydown', onKeydown))
  onUnmounted(() => window.removeEventListener('keydown', onKeydown))
  </script>
  
  <template>
    <div class="anime-detail">
      <div v-if="loading" class="loading">Загрузка...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
  
      <template v-else-if="media">

        <!-- BANNER -->
        <AnimeBanner
          :background="anime?.bannerImage || anime?.coverImage?.large"
        />
    
        <AnimeSideStats
          v-if="anime"
          :anime="anime"
        />

        <!-- MAIN INFO -->
        <div class="main-info-v2">
          <AnimePosterWithStatus
            v-if="anime"
            :cover="anime.coverImage?.extraLarge"
            @open-poster="openPoster"
          />
  
          <AnimeMainInfo :anime="media" />
        </div>
  
        <!-- DESCRIPTION -->
        <AnimeDescription :anime="media" />
  
        <!-- RELATIONS & STAFF -->
        <AnimeRelationsAndStaff :anime="media" />
  
        <!-- CHARACTERS -->
        <AnimeCharactersPreview
          v-if="anime && anime.characters?.edges.length"
          :characters="anime.characters.edges"
          :anime-id="anime.id"
        />

        <!-- SCREENSHOTS -->
        <AnimeScreenshotsGrid
          v-if="anime"
          :thumbnails="
            anime.streamingEpisodes
              ?.map(e => e.thumbnail)
              .filter((t): t is string => !!t) ?? []
          "
          :anime-id="anime.id"
          @open="openScreenshot"
        />
  
        <!-- TRAILER -->
        <AnimeTrailer
          v-if="anime"
          :trailer="anime.trailer"
        />
  
        <!-- DISCUSSION -->
        <AnimeDiscussion
          :media-id="media.id"
          :type="media.type"
        />
  
        <!-- MODALS -->
        <PosterModal
          v-if="posterOpen && anime"
          :src="anime.coverImage?.extraLarge"
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
  