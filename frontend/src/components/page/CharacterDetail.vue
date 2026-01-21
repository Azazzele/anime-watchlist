<script setup lang="ts">
  import { ref, computed, onMounted, watch } from 'vue'
  import { useRoute } from 'vue-router'
  import Card from '../ui/Card.vue'
  import VoiceActorCard from '../ui/character/VoiceActorCard.vue'
  
  const route = useRoute()
  
  const props = defineProps<{ characterId: string | number }>()
  const characterIdNum = computed(() => Number(props.characterId))
  
  const character = ref<any>(null)
  const loading = ref<boolean>(true)
  const error = ref<string | null>(null)
  
  const descriptionLang = ref<'ru' | 'en'>('en')
  const descriptionRu = ref<string | null>(null)
  
  const currentDescription = computed(() => {
    if (!character.value) return null
    return descriptionLang.value === 'ru' && descriptionRu.value
      ? descriptionRu.value
      : character.value.description_en || character.value.description || null
  })
  
  const toggleDescriptionLang = () => {
    descriptionLang.value = descriptionLang.value === 'ru' ? 'en' : 'ru'
  }
  
  const SHOW_LIMIT = 6
  const showAllAnime = ref(false)
  const visibleAnime = computed(() => {
    if (!Array.isArray(character.value?.anime)) return []
    const list = character.value.anime.filter((a: any) => a?.id)
    return showAllAnime.value ? list : list.slice(0, SHOW_LIMIT)
  })
  const getMediaType = (type?: string) => {
    if (type === 'MANGA') return 'manga'
    if (type === 'NOVEL') return 'ranobe'
    return 'anime'
  }

  const formatBirthDate = (dob: any) => {
    if (!dob || typeof dob !== 'object') return '—'
    const parts = [
      dob.day && String(dob.day),
      dob.month && ['января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря'][dob.month-1],
      dob.year && String(dob.year)
    ].filter(Boolean)
    return parts.join(' ') || '—'
  }

  const favourite = ref(false)
  const toggleFavourite = () => {
    favourite.value = !favourite.value

    if (character.value) {
      if (favourite.value) {
        character.value.favourites = (character.value.favourites || 0) + 1
      } else {
        character.value.favourites = Math.max((character.value.favourites || 1) - 1, 0)
      }
    }
  }

  const loadCharacter = async () => {
    loading.value = true
    error.value = null
  
    const id = characterIdNum.value
    if (isNaN(id) || id <= 0) {
      error.value = 'Некорректный ID персонажа'
      loading.value = false
      return
    }
  
    try {
      const res = await fetch(`http://127.0.0.1:8000/character/${id}`)
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data = await res.json()
  
      // --- фильтруем японскую актрису и берем только первую ---
      const japaneseVA = (data.voice_actors || []).filter((va:any) => va.language === 'Japanese')[0] || null
  
      character.value = {
        ...data,
        voice_actors: japaneseVA ? [japaneseVA] : []
      }
    } catch (err) {
      console.error('Ошибка загрузки персонажа:', err)
      error.value = 'Персонаж не найден или ошибка сервера'
      character.value = null
    } finally {
      loading.value = false
    }
  }
  
  onMounted(loadCharacter)
  watch(() => characterIdNum.value, loadCharacter, { immediate: true })
  </script>
  
  <template>
    <div class="character-page">
      <div v-if="character.favourites" class="stats" >
                <span class="heart material-symbols-outlined">favorite</span>
                {{ character.favourites.toLocaleString() }} избранных
          </div>
      <div v-if="loading" class="loading">Загрузка персонажа…</div>
      <div v-else-if="error" class="error">{{ error }}</div>
      <div v-else-if="character" class="content">
  
        <!-- HERO -->
        <section class="hero">
          <div class="avatar-wrap">
            <img v-if="character.image_large" :src="character.image_large" class="avatar" alt="Персонаж"/>
            <div v-else class="avatar-placeholder">Нет фото</div>

            <!-- Кнопка "В избранное" под постером -->
            <div class="poster-actions">
              <button
                class="fav-btn"
                :class="{ active: favourite }"
                @click="toggleFavourite"
              >
                <span class="material-symbols-outlined heart">favorite</span>
                {{ favourite ? 'В избранном' : 'В избранное' }}
              </button>
              
             
            </div>
          </div>

          <div class="hero-info-wrap">
            <div class="hero-info">
              <h2 class="hero-title">{{ character.name_full }}</h2>
              <p v-if="character.name_native" class="hero-native">{{ character.name_native }}</p>

              <ul>
                <li v-if="character.age"><span>Возраст:</span> {{ character.age }}</li>
                <li v-if="character.gender"><span>Пол:</span> {{ character.gender }}</li>
                <li v-if="character.bloodType"><span>Группа крови:</span> {{ character.bloodType }}</li>
                <li v-if="character.dateOfBirth"><span>Дата рождения:</span> {{ formatBirthDate(character.dateOfBirth) }}</li>
              </ul>

            </div>
           
            <!-- Сэйю (только японская) -->
            <section v-if="character.voice_actors?.length" class="voice-actors">
              <h2>Сэйю (Japanese)</h2>
              <div class="va-grid">
                <VoiceActorCard
                  v-for="actor in character.voice_actors"
                  :key="actor.id"
                  :actor="{
                    ...actor,
                    coverImage: actor.image
                  }"
                />
              </div>
            </section>
          </div>
        </section>
  
        <!-- Описание -->
        <section v-if="currentDescription" class="description-block">
          <div class="description-header">
            <h2>Описание</h2>
            <button class="lang-toggle" :disabled="!descriptionRu" @click="toggleDescriptionLang">
              <span class="material-symbols-outlined">{{ descriptionLang === 'ru' ? 'translate' : 'language' }}</span>
              <span class="lang-label">{{ descriptionLang.toUpperCase() }}</span>
            </button>
          </div>
          <div class="description-content" v-html="currentDescription" />
        </section>
  
        <!-- Аниме -->
        <section v-if="character.anime?.length" class="anime">
          <h2>Появляется в</h2>
          <div class="anime_wrapper">
            <Card
              v-for="anime in visibleAnime"
              :key="anime.id"
              :media="{
                id: anime.id,
                title: anime.title,
                cover_image_url: anime.coverImage?.large || anime.coverImage?.medium,
                format: anime.format ?? null,
                seasonYear: anime.seasonYear ?? null,
                averageScore: anime.averageScore ?? null
              }"
              :mediaType="getMediaType(anime.type)"
            />


          </div>
          <button v-if="character.anime.length > SHOW_LIMIT" class="show-more" @click="showAllAnime = !showAllAnime">
            {{ showAllAnime ? 'Скрыть' : 'Показать все' }} ({{ character.anime.length }})
          </button>
        </section>
      </div>
    </div>
  </template>
  
  
  <style scoped>  
  .avatar-placeholder {
    width: 260px;
    height: 360px;
    border-radius: 16px;
    background: #111827;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #64748b;
    font-size: 1.1rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
  }
  
  /* ... все остальные стили ... */
.character-page {
  max-width: 1240px;
  margin: 0 auto;
  padding: 32px 16px;
  color: #e5e7eb;
}

.loading,
.error {
  text-align: center;
  opacity: 0.7;
}
.hero-info-wrap {
  display: flex;
  gap: 32px;
  align-items: flex-start;
}


.avatar {
  width: 260px;
  border-radius: 16px;
  object-fit: cover;
  box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

.info h2 {
  font-size: 2.2rem;
  margin: 0;
}

.native {
  opacity: 0.7;
  margin-top: 6px;
}

.alt-names {
  margin-top: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.alt-names span {
  font-size: 0.75rem;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(255,255,255,0.08);
}

.favs {
  margin-top: 14px;
  font-weight: 600;
  color: #f87171;
}
.poster-actions {
  margin-top: 12px;
  display: flex;
  justify-content: center;
}

.fav-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 999px;
  border: none;
  cursor: pointer;
  background: transparent;
  
  color: #f87171;

  font-weight: 600;
  transition: all 0.2s ease;
}
.fav-btn.active {
  background: rgba(248, 113, 113, 0.15);
  color: #fff;
}
.fav-btn:hover {
  background: rgba(248, 113, 113, 0.25);
  transform: translateY(-1px);
}

.fav-btn span {
  font-size: 20px;
}

.description {
  line-height: 1.7;
  opacity: 0.9;
  margin-bottom: 40px;
}
.anime_wrapper{
	display: flex;
	flex-wrap: wrap;
	gap: 20px;
}
.anime h2 {
  margin-bottom: 16px;
}

.anime-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 16px;
}

.anime-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  text-decoration: none;
  color: inherit;
}

.anime-card img {
  border-radius: 12px;
  object-fit: cover;
  aspect-ratio: 3 / 4;
}

.anime-card span {
  font-size: 0.8rem;
  opacity: 0.85;
}
/* ===== Info block ===== */
.info-block {
  margin-bottom: 40px;
  
}
.voice-actors {
  margin-bottom: 48px;
}

.va-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.info-block h2 {
  margin-bottom: 12px;
}

.info-block ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-block li {
  display: flex;
  gap: 8px;
  opacity: 0.85;
  margin-bottom: 6px;
}

.info-block span {
  opacity: 0.6;
  min-width: 120px;
}

/* ===== Description ===== */
.description-block {
  margin-bottom: 48px;
  line-height: 1.8;
}

/* ===== Anime cards ===== */
.anime-card {
  background: #0d0f17;
  border-radius: 14px;
  padding: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.anime-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 14px 40px rgba(0,0,0,0.5);
}

.anime-card img {
  border-radius: 10px;
}

.anime-title {
  font-size: 0.8rem;
  margin-top: 6px;
  opacity: 0.9;
}

/* ===== Stats ===== */

.stats {
  display: flex;
  align-items: center;
  justify-content: end;
  gap: 6px;
  margin-left: 12px;
  font-weight: 600;
  color: #f87171;
  font-size: 0.9rem;
}

.heart {
color: #f87171;
  font-size: 20px;
}
/* ===== HERO ===== */
.hero {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 40px;
  margin-bottom: 48px;
}

.avatar-wrap {
  position: relative;
}

.avatar-wrap::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 18px;
  pointer-events: none;
}

.avatar {
  width: 100%;
  border-radius: 18px;
  object-fit: cover;
  box-shadow: 0 25px 60px rgba(0,0,0,0.55);
}

.hero-info {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.hero-title {
  font-size: 2.4rem;
  font-weight: 700;
  line-height: 1.1;
}

.hero-native {
  font-size: 1rem;
  opacity: 0.6;
}

/* ===== ALT NAMES ===== */
.alt-names {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 6px;
}

.alt-names span {
  font-size: 0.7rem;
  padding: 4px 10px;
  border-radius: 999px;
  backdrop-filter: blur(8px);
}

/* ===== STATS ===== */
.stats {
  margin-top: 14px;
  font-weight: 600;
  color: #f87171;
}

/* ===== INFO BLOCK ===== */
.info-block {
  background: #0b0d14;
  border-radius: 16px;
  padding: 20px 24px;
  margin-bottom: 48px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}

.info-block h2 {
  font-size: 1.1rem;
  margin-bottom: 16px;
}

.info-block li {
  display: grid;
  grid-template-columns: 140px 1fr;
  padding: 6px 0;
}

.info-block span {
  opacity: 0.55;
}

/* ===== DESCRIPTION ===== */
.description-block {
  background: #0b0d14;
  border-radius: 16px;
  padding: 28px;
  line-height: 1.8;
  margin-bottom: 56px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}
.description-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}
/* ===== ANIME GRID ===== */
.anime-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
}

.anime-card {
  background: #0d0f17;
  border-radius: 16px;
  padding: 10px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.anime-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 50px rgba(0,0,0,0.6);
}

.anime-card img {
  border-radius: 12px;
  aspect-ratio: 3 / 4;
  object-fit: cover;
}

.anime-title {
  font-size: 0.8rem;
  margin-top: 8px;
  opacity: 0.9;
  text-align: center;
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
.show-more {
  margin-top: 20px;
  padding: 10px 18px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,.15);
  background: rgba(255,255,255,.06);
  color: #cfd2ff;
  cursor: pointer;
  font-weight: 500;
}

.show-more:hover {
  background: rgba(255,255,255,.12);
}

/* ===== MOBILE ===== */
@media (max-width: 768px) {
  .hero {
    grid-template-columns: 1fr;
  }

  .avatar {
    max-width: 240px;
  }
}

	</style>