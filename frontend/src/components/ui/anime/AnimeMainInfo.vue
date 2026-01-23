<script setup lang="ts">
	import { computed } from 'vue'
	import type { Media } from '../../../types/type'
	import {
	  SEASONS,
	  FORMATS,
	  STATUS,
	  GENRES,
	  SOURCES,
	  t
	} from '../../../i18n/anilist.ru'
	
	const props = defineProps<{ anime?: Media | null }>()
	
	// Рейтинги по разным источникам
	const ratings = computed(() => ({
	  'Anilist': props.anime?.averageScore != null ? (props.anime.averageScore / 10).toFixed(1) : '—',
	  'MAL': props.anime?.malScore ?? '—',
	  'Shikimori': props.anime?.shikiScore ?? '—',
	}))

	// Функция для цвета рейтинга
	const ratingColor = (value: string) => {
	const num = parseFloat(value)
	if (isNaN(num)) return '#888' // серый для "—"
		// цвет от красного (#f87171) к зелёному (#4ade80)
		const r = Math.max(0, 248 - (num * 10))  // уменьшаем красный
		const g = Math.min(173 + (num * 15), 222) // увеличиваем зеленый
		const b = 113                          // синий оставим средним
		return `rgb(${Math.round(r)}, ${Math.round(g)}, ${b})`
	}

	const format = computed(() => t(FORMATS, props.anime?.format))
	const status = computed(() => t(STATUS, props.anime?.status))
	const season = computed(() => t(SEASONS, props.anime?.season))
	const genres = computed(() =>
	  props.anime?.genres?.map(g => t(GENRES, g)) ?? []
	)
	
	const source = computed(() => {
	  const s = props.anime?.source
	  if (!s || s === 'OTHER') return null
	  return t(SOURCES, s)
	})
	
	const score = computed(() =>
	  props.anime?.averageScore != null
		? (props.anime.averageScore / 10).toFixed(1)
		: '—'
	)
	
	const episodes = computed(() =>
	  props.anime?.episodes != null ? props.anime.episodes : '—'
	)
	</script>
	
	<template>
	<section v-if="anime" class="anime-info">
	
	  <!-- HEADER -->
	  <header class="header">
		<h2 class="title">{{ anime.title?.romaji }}</h2>
	
		<nav class="breadcrumbs">
		  <span class="crumb">{{ format }}</span>
		  <span class="sep">/</span>
		  <span class="crumb status">{{ status }}</span>
		  <span class="sep">/</span>
		  <span class="crumb season">{{ season }} {{ anime.seasonYear }}</span>
		</nav>
		
		<div v-if="genres.length" class="genres">
		  <span v-for="g in genres" :key="g">{{ g }}</span>
		</div>
	  </header>
	
	  <div class="content">
	
		<!-- LEFT -->
		<div class="main">
		  <section class="block">
			<h3>Альтернативные названия</h3>
			<div class="title-row">
			  <span class="label">Romaji</span>
			  <span class="value">{{ anime.title?.romaji || '—' }}</span>
			</div>
			<div v-if="anime.title?.english" class="title-row">
			  <span class="label">English</span>
			  <span class="value">{{ anime.title.english }}</span>
			</div>
		  </section>
	
		  <section class="block">
			<h3>Студия</h3>
			<p>{{ anime.studios?.nodes?.map(s => s.name).join(', ') || '—' }}</p>
		  </section>
	
		  <section v-if="source" class="block">
			<h3>Первоисточник</h3>
			<p>{{ source }}</p>
		  </section>
		</div>
	
		<!-- RIGHT / SIDEBAR -->
		<aside class="sidebar">
		  <!-- Рейтинги по источникам -->
		  	<div class="stat rating-sources">
				<div class="source" v-for="(value, key) in ratings" :key="key">
					<span class="source-name">{{ key }}</span>
					<b class="source-score" :style="{ color: ratingColor(value) }">{{ value ?? '—' }}</b>
				</div>
			</div>
		  <div class="stat">
			<span>Эпизоды</span>
			<b>{{ episodes }}</b>
		  </div>
	
		  <div class="stat">
			<span>Статус</span>
			<b>{{ status }}</b>
		  </div>
	
		  <div class="stat">
			<span>Комментариев</span>
			<b>0</b>
		  </div>
	
		  <div class="stat">
			<span>Рецензий</span>
			<b>0</b>
		  </div>
		</aside>
	
	  </div>
	</section>
	</template>
	
	<style scoped>
	.anime-info {
	  display: flex;
	  flex-direction: column;
	  gap: 28px;
	}
	
	/* HEADER */
	.header {
	  border-bottom: 1px solid rgba(255,255,255,.08);
	  padding-bottom: 20px;
	}
	
	.title {
	  font-size: 2.1rem;
	  font-weight: 700;
	}
	
	.breadcrumbs {
	  display: flex;
	  align-items: center;
	  gap: 8px;
	  font-size: 0.85rem;
	  color: #9ca3af;
	  margin-top: 12px;
	}
	
	.crumb { white-space: nowrap; }
	.sep { opacity: 0.4; }
	.status { color: #60a5fa; }
	.season { color: #a5b4fc; }
	
	.genres {
	  margin-top: 14px;
	  display: flex;
	  flex-wrap: wrap;
	  gap: 8px;
	}
	.genres span {
	  padding: 4px 12px;
	  border-radius: 999px;
	  font-size: .75rem;
	  background: rgba(99,102,241,.15);
	  color: #c7d2fe;
	}
	
	/* CONTENT */
	.content {
	  display: grid;
	  grid-template-columns: 1fr 260px;
	  gap: 32px;
	}
	
	/* MAIN */
	.main {
	  display: flex;
	  flex-direction: column;
	  gap: 20px;
	}
	.block h3 { font-size: .9rem; opacity: .6; margin-bottom: 6px; }
	.title-row { display: flex; gap: 12px; font-size: 0.85rem; line-height: 1.4; }
	.label { min-width: 70px; opacity: .55; }
	.value { font-weight: 500; color: #e5e7eb; }
	
	/* SIDEBAR */
	.sidebar {
	  border-left: 1px solid rgba(255,255,255,.08);
	  padding-left: 20px;
	  display: flex;
	  flex-direction: column;
	  gap: 12px;
	}
	
	.stat {
	  display: flex;
	  justify-content: space-between;
	  font-size: .85rem;
	}
	.stat span { opacity: .55; }
	
	/* Рейтинги по источникам */
	.rating-sources {
	  display: flex;
	  flex-wrap: wrap;
	  gap: 12px;
	  margin-bottom: 12px;
	}
	.rating-sources .source {
	  display: flex;
	  align-items: center;
	  gap: 4px;
	}
	.rating-sources .source-name { opacity: 0.6; }
	.rating-sources .source-score { font-weight: 600; }
	
	/* MOBILE */
	@media (max-width: 900px) {
	  .content { grid-template-columns: 1fr; }
	  .sidebar { border-left: none; padding-left: 0; }
	}
	</style>
	