<script setup lang="ts">
  import { ref, onMounted, computed } from 'vue'
  import Card from '../ui/Card.vue'
  import CharacterBithday from '../ui/CharacterBithday.vue'
  
  interface Anime {
    id: number
    title: {
      romaji?: string
      english?: string
      native?: string
    }
    coverImage?: {
      extraLarge?: string
      large?: string
      medium?: string
    }
    cover_image_url?: string
    format?: string | null
    seasonYear?: number | null
    averageScore?: number | null
  }
  
  /* ===================== SEASON ===================== */
  const seasonName = ref('')
  const seasonYear = ref('')
  
  function getCurrentSeason() {
    const now = new Date()
    const month = now.getMonth() + 1
    const year = now.getFullYear()
  
    if ([12, 1, 2].includes(month)) seasonName.value = 'Winter'
    else if ([3, 4, 5].includes(month)) seasonName.value = 'Spring'
    else if ([6, 7, 8].includes(month)) seasonName.value = 'Summer'
    else seasonName.value = 'Fall'
  
    const seasonYear = ref<number | null>(null)
    seasonYear.value = year

  }
  
  getCurrentSeason()
  
  /* ===================== STATE ===================== */
  const animes = ref<Anime[]>([])
  const loading = ref(true)
  const error = ref<string | null>(null)
  const notice = ref('')
  
  /* ===================== SHUFFLE ===================== */
  const shuffledAnimes = computed(() => {
    return [...animes.value].sort(() => Math.random() - 0.5)
  })
  
  /* ===================== LOAD ===================== */
  onMounted(async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/season/current')
      if (!res.ok) throw new Error('API error')
  
      const data = await res.json()
  
      if (Array.isArray(data)) {
        animes.value = data
  
        if (data.length === 0) {
          notice.value = `Сезон ${seasonName.value} ${seasonYear.value} только начался!
  Пока онгоингов мало, но скоро добавятся новые тайтлы 🔥`
        }
      } else if (data?.message) {
        notice.value = data.message
      }
    } catch {
      error.value = 'Не удалось загрузить текущий сезон'
    } finally {
      loading.value = false
    }
  })
  </script>
  
  <template>
    <section class="ongoing">
      <h2 class="title_header">
        Anime {{ seasonName }} {{ seasonYear }}
      </h2>
  
      <div v-if="loading" class="loading">Загрузка...</div>
      <div v-else-if="error" class="error">{{ error }}</div>
  
      <div v-else>
        <!-- NOTICE -->
        <div v-if="notice" class="season-notice">
          {{ notice }}
        </div>
  
        <!-- EMPTY -->
        <div v-else-if="animes.length === 0" class="empty">
          Пока список пустой — сезон только стартовал!
        </div>
  
        <!-- GRID -->
        <div v-else class="grid">
          <Card
            v-for="anime in shuffledAnimes"
            :key="anime.id"
            :media="{
              id: anime.id,
              title: anime.title,
              cover_image_url:
                anime.coverImage?.extraLarge ||
                anime.coverImage?.large ||
                anime.coverImage?.medium ||
                anime.cover_image_url ||
                null,
              format: anime.format ?? null,
              seasonYear: anime.seasonYear ?? null,
              averageScore: anime.averageScore ?? null
            }"
            mediaType="anime"
          />
        </div>
  
        <!-- BIRTHDAYS -->
        <CharacterBithday />
      </div>
    </section>
  </template>
  
  <style scoped>
  .title_header {
    font-size: 2rem;
    margin-bottom: 24px;
    text-align: center;
  }
  
  .season-notice {
    background: rgba(100, 181, 246, 0.2);
    color: #64b5f6;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 20px;
    text-align: center;
  }
  
  .empty {
    text-align: center;
    color: #aaa;
    font-size: 1.1em;
    padding: 40px 0;
  }
  
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    padding: 0 16px;
  }
  </style>
  