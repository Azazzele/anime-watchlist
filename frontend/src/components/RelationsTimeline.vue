<script setup lang="ts">
	import { computed } from 'vue'
	
	interface Relation {
	  relationType: string
	  node: {
		id: number
		format?: string
		startDate?: { year?: number }
		title: { romaji?: string; english?: string }
		coverImage?: { large?: string }
	  }
	}
	
	const props = defineProps<{
	  relations: { edges: Relation[] }
	}>()
	
	const items = computed(() =>
	  [...props.relations.edges].sort(
		(a, b) =>
		  (a.node.startDate?.year ?? 9999) -
		  (b.node.startDate?.year ?? 9999)
	  )
	)
	</script>
	
	<template>
		<section class="relations-row">
		  <h2 class="title">Связанное</h2>
	  
		  <div class="timeline">
			<div
			  v-for="rel in items"
			  :key="rel.node.id"
			  class="timeline-item"
			>
			  <!-- линия + точка -->
			  <div class="line-wrap">
				<span class="year">
				  {{ rel.node.startDate?.year || '—' }}
				</span>
				<span class="dot"></span>
			  </div>
	  
			  <!-- карточка -->
			  <router-link
				:to="`/anime/${rel.node.id}`"
				class="card-wrapper"
			  >
				<span class="badge">
				  {{ rel.relationType }}
				</span>
	  
				<div class="card">
				  <img
					:src="rel.node.coverImage?.large"
					class="cover"
				  />
	  
				  <div class="info">
					<h3>
					  {{ rel.node.title.romaji || rel.node.title.english }}
					</h3>
	  
					<div class="meta">
					  <span>{{ rel.node.format || '?' }}</span>
					</div>
				  </div>
				</div>
			  </router-link>
			</div>
	  
			<!-- общая линия -->
			<div class="base-line"></div>
		  </div>
		</section>
	  </template>
	  
	
	<style scoped>
.relations-row {
  max-width: 1600px;
  margin: 80px auto;
  padding: 0 32px;
}

.title {
  font-size: 1.5rem;
  margin-bottom: 32px;
}

/* контейнер таймлайна */
.timeline {
  position: relative;
  display: flex;
  gap: 48px;
  padding-top: 40px;
  overflow-x: auto;
}

/* базовая линия */
.base-line {
  position: absolute;
  top: 28px;
  left: 0;
  right: 0;
  height: 1px;
  background: #3a3f4b;
}


/* элемент */
.timeline-item {
  position: relative;
  min-width: 200px;
}

/* линия + точка */
.line-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 14px;
}

.year {
  font-size: 0.7rem;
  color: #9aa0ad;
  margin-bottom: 6px;
  letter-spacing: 0.04em;
}
 

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #c9ccd6;
}


/* карточка */
.card-wrapper {
  text-decoration: none;
  color: inherit;
  display: block;
}

.badge {
  position: absolute;
  top: 46px;
  left: 12px;
  font-size: 0.6rem;
  padding: 4px 8px;
  border-radius: 999px;
  background: linear-gradient(135deg, #6366f1, #a855f7);
  color: white;
  z-index: 2;
}

.card {
	width: 190px;
	background: #161922;
	border-radius: 14px;
	overflow: hidden;
	transition: transform 0.2s ease, background 0.2s ease;
}

.card:hover {
  transform: translateY(-6px);
  background: #1c2030;
}

.cover {
  width: 100%;
  aspect-ratio: 2 / 3;
  object-fit: cover;
}

.info {
  padding: 12px;
}

.info h3 {
  font-size: 0.85rem;
  line-height: 1.35;
  height: 2.7em;
  overflow: hidden;
}

.meta {
  font-size: 0.7rem;
  opacity: 0.7;
  margin-top: 6px;
}
.year-head {
  position: relative;
}

.year-head::before {
  content: '';
  position: absolute;
  top: 50%;
  left: -200px;
  right: -200px;
  height: 2px;
  background: rgba(99, 102, 241, 0.2);
  z-index: -1;
}
.line-wrap::after {
  content: '';
  width: 1px;
  height: 16px;
  background: #3a3f4b;
  margin-top: 6px;
}

	</style>
	