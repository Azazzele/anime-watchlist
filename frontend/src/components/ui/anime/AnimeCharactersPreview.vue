<script setup lang="ts">
	import { computed } from 'vue'
	
	interface CharacterEdge {
	  role: 'MAIN' | 'SUPPORTING' | string
	  node: {
		id: number
		name?: { full?: string }
		image?: { large?: string }
	  }
	}
	
	const props = defineProps<{
	  characters: CharacterEdge[]
	  animeId?: number
	  mediaType?: 'anime' | 'manga' | 'ranobe'
	}>()
	
	const previewCharacters = computed(() =>
	  props.characters
		.filter(c => c.role === 'MAIN' || c.role === 'SUPPORTING')
		.slice(0, 7)
	)
	
	const hasCharacters = computed(() => previewCharacters.value.length > 0)
	</script>
	
	<template>
	  <section v-if="hasCharacters" class="characters">
		<h2 class="title_header">Персонажи</h2>
	
		<div class="char-grid">
		  <!-- Персонажи -->
		  <router-link
			v-for="edge in previewCharacters"
			:key="edge.node.id"
			:to="{ name: 'character', params: { characterId: edge.node.id } }"
			class="char-card"
		  >
			<img
			  v-if="edge.node.image?.large"
			  :src="edge.node.image.large"
			  class="char-img"
			/>
			<div v-else class="char-placeholder">Нет фото</div>
	
			<p class="char-name">
			  {{ edge.node.name?.full || '???' }}
			</p>
		  </router-link>
	
		 <!-- Все персонажи -->
		<router-link
		v-if="animeId && mediaType && characters.length > previewCharacters.length"

			:to="`/${mediaType}/${animeId}/characters`"
			class="char-card show-all"
			>
			<span class="material-symbols-outlined">group</span>
			<p>Все персонажи</p>
		</router-link>

		</div>
	  </section>
	</template>
	
	<style scoped>
		
.characters {
  margin-top: 48px;
}

.char-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-items: start;
  align-self: stretch;
  justify-content: start;
  margin-left: 3em;
  
}

.char-card {
  width: 175px;
  display: flex;
  height: 100%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  margin: 0 1em;
  color: inherit;
  border-radius: 14px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.char-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.45);
}

.char-img {
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 8px;
  height: 310px;
}

.char-placeholder {
  width: 100%;
  border-radius: 10px;
  background: #0b0d14;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  font-size: 0.85rem;
  margin-bottom: 8px;
}

.char-name {
  font-size: 1.2rem;
  text-align: center;
  line-height: 1.3;
  opacity: 0.9;
  word-break: keep-all;
}

/* карточка "Все персонажи" */
.char-card.show-all {
  justify-content: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.06);
}

.char-card.show-all span {
  font-size: 32px;
  opacity: 0.7;
}

.char-card.show-all p {
  font-size: 0.8rem;
  opacity: 0.8;
}

/* адаптив */
@media (max-width: 768px) {
  .char-grid {
    justify-content: center;
  }

  .char-card {
    width: 120px;
  }
}

	</style>
	