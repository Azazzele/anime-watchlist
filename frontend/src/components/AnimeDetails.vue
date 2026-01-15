<script setup lang="ts">
  import { ref, watch, onMounted, onUnmounted } from 'vue'
  import { useRoute } from 'vue-router'
  
  const route = useRoute()
  
  const anime = ref<any>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)
  
  /* ===== USER STATE ===== */
  /* ================= POSTER ================= */
  const isPosterOpen = ref(false)

  const openPoster = () => {
    isPosterOpen.value = true
    document.body.style.overflow = 'hidden'
  }

  const closePoster = () => {
    isPosterOpen.value = false
    document.body.style.overflow = ''
  }

  const onKey = (e: KeyboardEvent) => {
    if (e.key === 'Escape') closePoster()
  }

  onMounted(() => window.addEventListener('keydown', onKey))
  onUnmounted(() => window.removeEventListener('keydown', onKey))

  /* ================= USER ACTIONS ================= */
  type Status =
    | 'watching'
    | 'planned'
    | 'completed'
    | 'paused'
    | 'dropped'
    | null

  const userStatus = ref<Status>(null)
  const favorite = ref(false)
  const menuOpen = ref(false)

  const setStatus = (status: Status) => {
    userStatus.value = status
    menuOpen.value = false
  }

  const toggleFavorite = () => {
    favorite.value = !favorite.value
  }

  const toggleMenu = () => {
    menuOpen.value = !menuOpen.value
  }

  const userStatusLabel = (status: Status) => {
    switch (status) {
      case 'watching': return 'Смотрю'
      case 'planned': return 'В планах'
      case 'completed': return 'Просмотрено'
      case 'paused': return 'Отложено'
      case 'dropped': return 'Заброшено'
      default: return 'Выбрать статус'
    }
  }

  const onClickOutside = (e: MouseEvent) => {
    const target = e.target as HTMLElement
    if (!target.closest('.status-dropdown')) {
      menuOpen.value = false
    }
  }

  onMounted(() => document.addEventListener('click', onClickOutside))
  onUnmounted(() => document.removeEventListener('click', onClickOutside))


  /* ===== DATA LOAD ===== */
  const loadAnime = async (id: number) => {
    loading.value = true
    error.value = null
  
    try {
      const res = await fetch(`http://127.0.0.1:8000/anime/${id}`)
      if (!res.ok) throw new Error()
      anime.value = await res.json()
    } catch {
      error.value = 'Ошибка загрузки данных аниме'
    } finally {
      loading.value = false
    }
  }
  
  watch(
    () => route.params.id,
    (id) => loadAnime(Number(id)),
    { immediate: true }
  )
  </script>
  
  <template>
    <div class="anime-detail">
      <div v-if="loading" class="loading">Загрузка...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
  
      <div v-else-if="anime">
        <!-- BANNER -->
        <div
          class="banner"
          :style="{ backgroundImage: `url(${anime.bannerImage || anime.coverImage?.large})` }"
        />
  
        <!-- MAIN INFO -->
        <div class="main-info">
          <!-- LEFT COLUMN -->
          <div class="poster-column">
            <img
              :src="anime.coverImage?.extraLarge"
              class="cover clickable"
              @click="openPoster"
            />
  
            <div class="poster-actions">
      <!-- DROPDOWN -->
      <div class="status-dropdown">
        <button class="action-btn" @click.stop="toggleMenu">
          <span class="material-symbols-outlined">expand_more</span>
          {{ userStatusLabel(userStatus) }}
        </button>

        <div v-if="menuOpen" class="dropdown-menu">
          <button @click="setStatus('watching')">
            <span class="material-symbols-outlined">play_arrow</span>
            Смотрю
          </button>

          <button @click="setStatus('planned')">
            <span class="material-symbols-outlined">schedule</span>
            В планах
          </button>

          <button @click="setStatus('completed')">
            <span class="material-symbols-outlined">done</span>
            Просмотрено
          </button>

          <button @click="setStatus('paused')">
            <span class="material-symbols-outlined">pause</span>
            Отложено
          </button>

          <button @click="setStatus('dropped')">
            <span class="material-symbols-outlined">close</span>
            Заброшено
          </button>
        </div>
      </div>

      <!-- FAVORITE (ОТДЕЛЬНО) -->
      <button
        class="fav-btn"
        :class="{ active: favorite }"
        @click="toggleFavorite"
      >
        <span class="material-symbols-outlined">
          {{ favorite ? 'star' : 'star_outline' }}
        </span>
      </button>
    </div>
          </div>
  
          <!-- RIGHT COLUMN -->
          <div class="details">
            <h2>{{ anime.title.romaji }}</h2>
            <p v-if="anime.title.english" class="alt-title">
              {{ anime.title.english }}
            </p>
  
            <div class="tags">
              <span class="tag">{{ anime.format || '?' }}</span>
              <span class="tag">{{ anime.status || '?' }}</span>
              <span class="tag">{{ anime.seasonYear || '?' }}</span>
              <span class="tag score">
                {{ anime.averageScore ? (anime.averageScore / 10).toFixed(1) : '?' }}
              </span>
            </div>
  
            <p class="description" v-html="anime.description || 'Описание отсутствует'" />
  
            <div class="genres">
              <span v-for="g in anime.genres" :key="g" class="genre">{{ g }}</span>
            </div>
  
            <div class="studios">
              Студии:
              {{ anime.studios.nodes?.map(s => s.name).join(', ') || '?' }}
            </div>
          </div>
        </div>
  
        <!-- CHARACTERS -->
        <section class="characters">
          <h2 class='title_header'>Персонажи</h2>
          <div class="char-grid">
            <div
              v-for="edge in anime.characters.edges"
              :key="edge.node.id"
              class="char-item"
            >
              <img :src="edge.node.image.large" />
              <p>{{ edge.node.name.full }}</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  
    <!-- POSTER MODAL -->
    <div v-if="isPosterOpen" class="poster-overlay" @click.self="closePoster">
      <img
        :src="anime.coverImage?.extraLarge"
        class="poster-full"
        @click="closePoster"
      />
    </div>  
  </template>
  
  <style scoped>
  .anime-detail {
    background: radial-gradient(1200px 600px at top, #121526, #07080f);
    min-height: 100vh;
    color: #e6e6eb;
  }
  
  /* BANNER */
  .banner {
    height: 360px;
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
    background: linear-gradient(135deg, #6366f1, #a855f7);
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
    background: rgba(22, 24, 43, 0.55);
    backdrop-filter: blur(18px);
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
    margin: 80px auto;
    padding: 0 32px;
  }
  
  .char-grid {
    display: flex;
    width: 100%;
    flex-wrap: wrap;
    gap: 16px;
    justify-content: center;
  }
  
  .char-item img {
    width: 200px;
    border-radius: 12px;
  }
  
  /* POSTER OVERLAY */
  .poster-overlay {
    position: fixed;
    inset: 0;
    background: rgba(10,5,20,0.9);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
  }
  
  .poster-full {
    max-width: 90vw;
    max-height: 90vh;
    border-radius: 18px;
    cursor: zoom-out;
  }
  </style>
  