<script setup lang="ts">
  import { ref, watch, onMounted, onUnmounted, computed } from 'vue'
  import { useRoute } from 'vue-router'
  import RelationsRow from './RelationsTimeline.vue'

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
  const characters = computed(() => {
  if (!anime.value?.characters?.edges) return []

  return anime.value.characters.edges
    .filter(
      (c: any) => c.role === 'MAIN' || c.role === 'SUPPORTING'
    )
    .slice(0, 6)
})
 

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
        <div class="main-info-v2">
  <!-- POSTER -->
  <div class="poster-wrap">
    <img
      :src="anime.coverImage?.extraLarge"
      class="poster"
      @click="openPoster"
    />
  </div>

  <!-- CONTENT -->
  <div class="content-wrap">
    <!-- TITLE -->
    <div class="title-row">
      <h1>{{ anime.title.romaji }}</h1>
      <span class="year">
        {{ anime.startDate?.year }}–{{ anime.endDate?.year || '...' }}
      </span>
    </div>

    <p v-if="anime.title.english" class="alt-title">
      {{ anime.title.english }}
    </p>

    <!-- META STRIP -->
    <div class="meta-strip">
      <span>{{ anime.format }}</span>
      <span>{{ anime.status }}</span>
      <span>{{ anime.episodes || '?' }} ep</span>
      <span>{{ anime.averageScore ? (anime.averageScore / 10).toFixed(1) : '—' }} ★</span>
    </div>
    
    <!-- ACTION ICONS -->
    <div class="actions-row">
      <button title="В избранное"><span class="material-symbols-outlined">star</span></button>
      <button title="Комментарий"><span class="material-symbols-outlined">comment</span></button>
      <button title="Отзыв"><span class="material-symbols-outlined">rate_review</span></button>
      <button title="В плейлист"><span class="material-symbols-outlined">playlist_add</span></button>
      <button title="Поделиться"><span class="material-symbols-outlined">share</span></button>
      <button title="Смотреть"><span class="material-symbols-outlined">play_circle</span></button>
    </div>
    <div class='genres'>
        <strong>Жанры:</strong>
        <div class="genre">{{ anime.genres.join(', ') }}</div>
      </div>
    <!-- DESCRIPTION -->
    <div class="description" v-html="anime.description"></div>

    <!-- FOOTER -->
    <div class="footer-info">
      <div class="studios">
        <strong>Студии:</strong>
        {{ anime.studios.nodes.map(s => s.name).join(', ') }}
      </div>
    
    </div>
  </div>
</div>


        <!-- RELATIONS -->
        <RelationsRow
          v-if="anime.relations?.edges?.length"
          :relations="anime.relations"
        />
          
        <!-- CHARACTERS -->
        <section class="characters">
          <h2 class='title_header'>Персонажи</h2>
          <div class="char-grid">
            <div
              v-for="edge in characters"
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
    width: 1480px;
    margin: 80px auto;
    padding: 0 32px;
  }
  
  .char-grid {
    display: flex;
    width: 100%;
    flex-wrap: wrap;
    gap: 16px;
    justify-content:baseline;
  }
  .char-item{
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .char-item img {
    width: 220px;
    height: 340px;
    border-radius: 12px;
  }
  .char-item p{
    margin-top: .6em;
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
  max-width: 1860px;
  margin: -120px auto 0;
  padding: 32px;
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 48px;
  background: rgba(15, 18, 32, 0.55);
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
  color: #cfd2ff;
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
  color: #cfd2ff;
}

.actions-row button:hover {
  background: rgba(255,255,255,.1);
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
  backdrop-filter: blur(8px);
}
.genres {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
  margin: 14px 0 18px;
}
.genre {
  font-size: 1.02rem;
  padding: 5px 12px;
  border-radius: 999px;

  background: linear-gradient(
    135deg,
    rgba(99,102,241,0.18),
    rgba(168,85,247,0.18)
  );

  color: #c7c9ff;
  letter-spacing: 0.3px;
  text-transform: uppercase;

  border: 1px solid rgba(255,255,255,0.08);
}

  </style>
  