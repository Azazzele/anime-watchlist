<script setup lang="ts">
	import { computed } from 'vue'
	
	const props = defineProps<{ trailer?: any }>()
	
	const trailerUrl = computed(() => {
	  if (!props.trailer || props.trailer.site !== 'youtube') return null
	  return `https://www.youtube.com/embed/${props.trailer.id}`
	})
	</script>
	
	<template>
	<h2 class='title_header'>Трейлер и прочие связанные видео</h2>
	  <section v-if="trailerUrl" class="media-section">
		<div class="trailer-wrap">
		  <iframe :src="trailerUrl" title="Trailer" allowfullscreen />
		</div>
	  </section>
	</template>
	
	<style scoped>
	.media-section {
    display: flex;
    padding: 0 16px;
    justify-content: start;
}

/* Контейнер трейлера */
.trailer-wrap {
	
  position: relative;
  max-width: 560px;    
  margin-left: 30px;           
  aspect-ratio: 16 / 9;    
  overflow: hidden;
  border-radius: 24px;

  background: #0b0d14;
  box-shadow:
    0 20px 40px rgba(0, 0, 0, 0.45),
    inset 0 0 0 1px rgba(255, 255, 255, 0.06);
}

/* iframe */
.trailer-wrap iframe {
  width: 100%;
  height: 100%;
  border: none;
}

/* Мобильная адаптация */
@media (max-width: 768px) {
  .media-section {
    margin: 56px auto;
  }

  .title_header {
    font-size: 1.5rem;
    text-align: center;
  }

  .trailer-wrap {
    border-radius: 18px;
  }
}

	</style>