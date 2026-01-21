<script setup lang="ts">
	import { computed } from 'vue'
	
	const props = defineProps<{ trailer?: any }>()
	
	const trailerUrl = computed(() => {
	  if (!props.trailer || props.trailer.site !== 'youtube') return null
	  return `https://www.youtube.com/embed/${props.trailer.id}`
	})
	</script>
	
	<template>
	  <section v-if="trailerUrl" class="media-section">
		<h2 class='title_header'>Трейлер</h2>
		<div class="trailer-wrap">
		  <iframe :src="trailerUrl" title="Trailer" allowfullscreen />
		</div>
	  </section>
	</template>
	
	<style scoped>
	.media-section {
	  max-width: 480px;
	  margin: 80px auto;
	  padding: 0 32px;
	}
	
	.trailer-wrap {
	  position: relative;
	  padding-bottom: 56.25%; /* 16:9 */
	  height: 0;
	  overflow: hidden;
	  border-radius: 30px;
	  border-color: none !important;
	  margin-bottom: 10.5em;
	}
	
	.trailer-wrap iframe {
	  position: absolute;
	  top: 0;
	  left: 0;
	  width: 100%;
	  height: 100%;
	}
	</style>