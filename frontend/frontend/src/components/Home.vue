<script setup>
  import { ref, onMounted, computed  } from 'vue'
  import Card from './Card.vue'
  import CharacterBithday from './CharacterBithday.vue' 
  
  const seasonName = ref('')
  const seasonYear = ref('')
  const shuffledAnimes = computed(() => {
  return [...animes.value].sort(() => Math.random() - 0.5)
})

  function getCurrentSeason() {
    const now = new Date()
    const month = now.getMonth() + 1
    const year = now.getFullYear()
    
    let season = ''
    if ([12, 1, 2].includes(month)) season = 'Winter'
    else if ([3, 4, 5].includes(month)) season = 'Spring'
    else if ([6, 7, 8].includes(month)) season = 'Summer'
    else season = 'Fall'
  
    seasonName.value = season
    seasonYear.value = year
  }
  
  getCurrentSeason()
  
  const animes = ref([])
  const loading = ref(true)
  const error = ref(null)
  const notice = ref('')
  
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
      } else if (data.message) {
        notice.value = data.message
      }
    } catch (e) {
      error.value = 'Не удалось загрузить текущий сезон'
    } finally {
      loading.value = false
    }
  })
  </script>
  
  <template>
    <section class="ongoing">
      <h2 class="title_header">Anime {{ seasonName }} {{ seasonYear }}</h2>
  
      <div v-if="loading" class="loading">Загрузка...</div>
  
      <div v-else-if="error" class="error">{{ error }}</div>
  
      <div v-else>
          <!-- Уведомление -->
          <div v-if="notice" class="season-notice">
            {{ notice }}
          </div>

          <!-- Пусто ТОЛЬКО если нет notice -->
          <div v-else-if="animes.length === 0" class="empty">
            Пока список пустой — сезон только стартовал!
          </div>

  
        <!-- Список аниме (если есть) -->
        <div v-else class="grid">
          <Card
            v-for="anime in shuffledAnimes"
            :key="anime.id"
            :anime="anime"
          />
        </div>
  
  
        <!-- Блок персонажей с ДР -->
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
  
  .separator {
    height: 1px;
    background: #333;
    margin: 40px 0;
  }
  
  /* Остальные стили карточек и т.д. — оставляй как были */
  </style>