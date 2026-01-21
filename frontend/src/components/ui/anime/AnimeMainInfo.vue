<script setup lang="ts">
	import { computed } from 'vue'
	import { Media } from '../../../types/type';

	
	const props = defineProps<{
	  anime: Media | null | undefined
	}>()
	
	const ratings = computed(() => {
	  const score = props.anime?.averageScore
	
	  return {
		anilist: score != null ? (score / 10).toFixed(1) : null,
		kinopoisk: null,
		shikimori: null,
	  }
	})
	const quantityLabel = computed(() => {
	const media = props.anime
	if (!media) return '—'

	switch (media.type) {
		case 'ANIME':
		return media.episodes != null
			? `${media.episodes} эп.`
			: '—'

		case 'MANGA':
		case 'NOVEL': {
		const parts: string[] = []

		if (media.volumes != null) {
			parts.push(`${media.volumes} том${media.volumes > 1 ? 'а' : ''}`)
		}

		if (media.chapters != null) {
			parts.push(`${media.chapters} глав`)
		}

		return parts.length ? parts.join(', ') : '—'
		}

		default:
		return '—'
	}
	})


	</script>
	
	<template>
	  <div v-if="anime" class="content-wrap">
		<div class="title-row">
		  <h2>{{ anime.title?.romaji || 'Без названия' }}</h2>
		</div>
	
		<p v-if="anime.title?.english" class="alt-title">
		  {{ anime.title.english }}
		</p>
		<p v-if="anime.title?.native" class="alt-title">
		  {{ anime.title.native }}
		</p>
	
		<div class="meta-strip">
			<span>{{ anime.format || '?' }}</span>
			<span>{{ anime.status || '?' }}</span>
			<span>{{ quantityLabel }}</span>
		</div>
	
		<div class="rating-sources">
		  <div v-if="ratings.anilist" class="rating-badge anilist">
			<span class="source">AniList</span>
			<span class="value">{{ ratings.anilist }}</span>
		  </div>
	
		  <div class="rating-badge kinopoisk disabled">
			<span class="source">КиноПоиск</span>
			<span class="value">—</span>
		  </div>
	
		  <div class="rating-badge shikimori disabled">
			<span class="source">Shikimori</span>
			<span class="value">—</span>
		  </div>
		</div>
	
		<div class="meta-secondary">
		  <span>{{ anime.season || '?' }} / {{ anime.seasonYear ?? '?' }}</span>
		</div>
	
		<div class="actions-row">
		  <button title="В избранное">
			<span class="material-symbols-outlined">bookmark</span>
		  </button>
		  <button title="Комментарий">
			<span class="material-symbols-outlined">comment</span>
		  </button>
		  <button title="Отзыв">
			<span class="material-symbols-outlined">rate_review</span>
		  </button>
		  <button title="В плейлист">
			<span class="material-symbols-outlined">playlist_add</span>
		  </button>
		  <button title="Поделиться">
			<span class="material-symbols-outlined">share</span>
		  </button>
		  <button title="Смотреть">
			<span class="material-symbols-outlined">play_circle</span>
		  </button>
		</div>
	
		<div v-if="anime.genres?.length" class="genres">
		  <strong>Жанры:</strong>
		  <div class="genre-list">
			<span
			  v-for="genre in anime.genres"
			  :key="genre"
			  class="genre"
			>
			  {{ genre }}
			</span>
		  </div>
		</div>
	
		<div class="footer-info">
		  <div v-if="anime.studios?.nodes?.length" class="studios">
			<h2>Студия:</h2>
			<h3>{{ anime.studios.nodes.map(s => s.name).join(', ') }}</h3>
		  </div>
		</div>
	  </div>
	
	  <!-- опционально: заглушка, если anime не пришёл -->
	  <div v-else class="content-wrap empty">
		<p>Данные об аниме не загружены</p>
	  </div>
	</template>
	
	<style scoped>
	.content-wrap {
	  position: relative;
	}
	
	.title-row h2 {
	  font-weight: 600;
	  letter-spacing: 0.2px;
	  display: -webkit-box;
	  -webkit-line-clamp: 3;
	  -webkit-box-orient: vertical;
	  overflow: hidden;
	  text-overflow: ellipsis;
	  margin: 0;
	}
	
	.alt-title {
	  margin-top: 4px;
	  opacity: 0.6;
	  margin-bottom: 0;
	}
	
	.meta-strip {
	  display: flex;
	  flex-wrap: wrap;
	  gap: 14px;
	  margin: 20px 0;
	  font-size: 0.85rem;
	}
	
	.meta-strip span {
	  padding: 6px 14px;
	  background: rgba(255, 255, 255, 0.05);
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
	  background: rgba(255, 255, 255, 0.06);
	  color: #e5e7eb;
	  border: 1px solid rgba(255, 255, 255, 0.12);
	}
	
	.actions-row {
	  display: flex;
	  flex-wrap: wrap;
	  gap: 12px;
	  margin-bottom: 26px;
	}
	
	.actions-row button {
	  width: 42px;
	  height: 42px;
	  border-radius: 10px;
	  background: rgba(255, 255, 255, 0.04);
	  border: 1px solid rgba(255, 255, 255, 0.06);
	  color: #e6e6eb;
	  cursor: pointer;
	  display: flex;
	  align-items: center;
	  justify-content: center;
	  transition: background 0.2s ease;
	}
	
	.actions-row button:hover {
	  background: rgba(255, 255, 255, 0.1);
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
	  border: 1px solid rgba(255, 255, 255, 0.08);
	  background: rgba(255, 255, 255, 0.03);
	}
	
	.footer-info {
	  margin-top: 26px;
	  font-size: 0.85rem;
	  color: #9ca3af;
	}
	
	.studios {
	  position: absolute;
	  top: 0;
	  right: 0;
	  font-size: 1.75rem;
	  color: #aab0ff;
	  opacity: 0.85;
	  text-align: right;
	}
	
	.rating-sources {
	  display: flex;
	  flex-wrap: wrap;
	  gap: 12px;
	  margin: 12px 0 1em;
	}
	
	.rating-badge {
	  display: inline-flex;
	  align-items: center;
	  gap: 6px;
	  padding: 4px 10px;
	  border-radius: 8px;
	  font-size: 0.78rem;
	  font-weight: 500;
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
	
	/* Цвета по источникам */
	.rating-badge.anilist {
	  border-color: rgba(59, 130, 246, 0.45);
	  color: #93c5fd;
	}
	
	.rating-badge.kinopoisk {
	  border-color: rgba(245, 158, 11, 0.45);
	  color: #facc15;
	}
	
	.rating-badge.shikimori {
	  border-color: rgba(239, 68, 68, 0.45);
	  color: #fca5a5;
	}
	
	.rating-badge.disabled {
	  opacity: 0.35;
	  border-style: dashed;
	}
	
	/* Заглушка, если данных нет */
	.content-wrap.empty {
	  opacity: 0.6;
	  text-align: center;
	  padding: 40px 0;
	}
	</style>