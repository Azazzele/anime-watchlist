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
	  mediaId?: number
	  mediaType?: 'anime' | 'manga' | 'ranobe'
	}>()
	
	const previewCharacters = computed(() =>
	  props.characters
		.filter(c => c.role === 'MAIN' || c.role === 'SUPPORTING')
		.slice(0, 6)
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
			v-if="mediaId && mediaType"
			:to="`/${mediaType}/${mediaId}/characters`"
			class="char-card show-all"
		  >
			<span class="material-symbols-outlined">group</span>
			<p>Все персонажи</p>
		  </router-link>
		</div>
	  </section>
	</template>
	
	<style scoped>
	/* стили без изменений — они норм */
	</style>
	