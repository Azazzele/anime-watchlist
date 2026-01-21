  
  <script setup lang="ts">
	import { computed } from 'vue'
	import type { MediaMini, CharacterMini } from '../../../types/user'
	
	const props = defineProps<{
	  title: string
	  items: (MediaMini | CharacterMini)[]
	  type: 'anime' | 'manga' | 'character' | 'staff'
	}>()
	const isMedia = (item: MediaMini | CharacterMini): item is MediaMini => {
		return 'title' in item
	}
	
	const visibleItems = computed(() => props.items.slice(0, 12))
	const hasMore = computed(() => props.items.length > 12)
	
	const getImage = (item: MediaMini | CharacterMini) => {
		if (isMedia(item)) {
			return item.coverImage?.large || '/placeholder.png'
		}

		return item.image?.large || '/placeholder.png'
	}

	
	const getName = (item: MediaMini | CharacterMini) => {
		if (isMedia(item)) {
			return (
			item.title.userPreferred ||
			item.title.romaji ||
			'Без названия'
			)
		}

		return item.name.full || 'Без имени'
	}

	
	const linkTo = (item: MediaMini | CharacterMini) => {
		if (isMedia(item)) {
			return `/${props.type}/${item.id}`
		}

		return `/character/${item.id}`
	}

	</script>
	
<template>
	<div class="section favourites">
	  <h2 class="section-title">{{ title }}</h2>
  
	  <div v-if="items.length" class="grid">
		<router-link
		  v-for="item in visibleItems"
		  :key="item.id"
		  :to="linkTo(item)"
		  class="fav-card"
		>
		  <div class="poster">
			<img
			  :src="getImage(item)"
			  :alt="getName(item)"
			  loading="lazy"
			/>
		  </div>
		  <p class="name">{{ getName(item) }}</p>
		</router-link>
	  </div>
  
	  <p v-if="hasMore" class="more-text">
		+ ещё {{ items.length - 12 }}
	  </p>
	</div>
  </template>

  <style scoped>
  .section {
	background: white;
	border-radius: 12px;
	padding: 1.8rem;
	margin-bottom: 1.8rem;
	box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  }
  
  .section-title {
	font-size: 1.5rem;
	font-weight: bold;
	margin-bottom: 1.2rem;
	color: #6366f1;
  }
  
  .grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
	gap: 1.2rem;
  }
  
  .fav-card {
	text-decoration: none;
	color: inherit;
	transition: transform 0.2s ease;
  }
  
  .fav-card:hover {
	transform: translateY(-6px);
  }
  
  .poster {
	aspect-ratio: 2/3;
	border-radius: 10px;
	overflow: hidden;
	box-shadow: 0 6px 15px rgba(0,0,0,0.15);
	background: #e5e7eb;
  }
  
  .poster img {
	width: 100%;
	height: 100%;
	object-fit: cover;
  }
  
  .name {
	margin-top: 0.6rem;
	font-size: 0.95rem;
	line-height: 1.3;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
	text-align: center;
  }
  
  .more-text {
	text-align: center;
	margin-top: 1rem;
	color: #6c757d;
	font-size: 0.95rem;
  }
  </style>