<script setup lang="ts">
	import { computed } from 'vue'

	interface Anime {
		id: number
		title: { romaji?: string; english?: string }
		cover_image_url?: string | null
		format?: string | null
		seasonYear?: number | null
		averageScore?: number | null
	}

	const props = defineProps<{ anime: Anime }>()

	const posterUrl = computed<string>(() => {
		return props.anime.cover_image_url ?? '/img/placeholder.png'
	})

	const onImageError = (e: Event) => {
		(e.target as HTMLImageElement).src = '/img/placeholder.png'
	}

	</script>
	
	<template>
		<router-link
			:to="`/anime/${props.anime.id}`"
			class="poster-link"
			@click="console.log('CLICK', props.anime.id)"
			>
		<article class="card">
			<div class="poster">
			<img
				:src="posterUrl"
				:alt="props.anime.title?.romaji || 'Аниме'"
				loading="lazy"
				@error="onImageError"
			/>
			</div>
		
			<div class="info">
			<h3 class="title">
				{{ props.anime.title?.romaji || props.anime.title?.english || 'Без названия' }}
			</h3>
		
			<div class="meta">
				<span class="year">{{ props.anime.seasonYear || '—' }}</span>
				<span class="score">{{ props.anime.averageScore ? (props.anime.averageScore / 10).toFixed(1) : '—' }}</span>
			</div>
			</div>
		</article>
		</router-link>
	</template>
	
	<style scoped>
	.card {
	  width: 220px;
	  background: #0d0f17;
	  border-radius: 12px;
	  overflow: hidden;
	  transition: transform 0.2s ease, box-shadow 0.2s ease;
	}
	
	.card:hover {
	  transform: translateY(-6px);
	  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.5);
	}
	
	.poster {
	  width: 100%;
	  aspect-ratio: 3 / 4;
	}
	
	.poster img {
	width: 220px;
	  height:320px;
	  object-fit: cover;
	  display: block;
	}
	
	.info {
	  padding: 12px 10px;
	  text-align: center;
	}
	
	.title {
	  font-size: 0.95rem;
	  font-weight: 500;
	  margin: 0 0 8px;
	  line-height: 1.3;
	  color: #e0e0e0;
	  height: 2.6em;
	  overflow: hidden;
	  display: -webkit-box;
	  -webkit-box-orient: vertical;
	}
	
	.meta {
	  display: flex;
	  justify-content: space-between;
	  align-items: center;
	  font-size: 0.78rem;
	  color: #8a8f9e;
	}
	
	.score {
	  font-weight: 600;
	  color: #a0d911;
	}
	</style>