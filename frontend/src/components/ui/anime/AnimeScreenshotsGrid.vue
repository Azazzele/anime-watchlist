<script setup lang="ts">
	import { computed } from 'vue'
	
	const props = defineProps<{
	  thumbnails: string[]
	  animeId: number
	}>()
	
	defineEmits(['open'])
	
	const previewScreenshots = computed(() => props.thumbnails.slice(0, 6))
	const hasMoreScreenshots = computed(() => props.thumbnails.length > 6)
	</script>
	
	<template>
	  <section v-if="thumbnails.length" class="media-section">
		<h2 class='title_header'> Скриншоты</h2>
		<div class="screenshots-grid">
		  <img
			v-for="(img, i) in previewScreenshots"
			:key="i"
			:src="img"
			class="screenshot"
			@click="$emit('open', img)"
		  />
	
		  <router-link
			v-if="hasMoreScreenshots"
			:to="`/anime/${animeId}/screenshots`"
			class="screenshot show-all-screens"
		  >
			<span class="material-symbols-outlined">collections</span>
			<span>Все скриншоты</span>
		  </router-link>
		</div>
	  </section>
	</template>
	
	<style scoped>
	.media-section {
	  margin: 80px auto;
	  padding: 0 32px;
	}
	
	.screenshots-grid {
	  display: grid;
	  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
	}
	
	.screenshot {
	  width: 100%;
	  aspect-ratio: 16 / 9;
	  object-fit: cover;
	  border-radius: 14px;
	  cursor: zoom-in;
	  transition: transform .2s ease, box-shadow .2s ease;
	}
	
	.screenshot:hover {
	  transform: scale(1.03);
	  box-shadow: 0 20px 50px rgba(0,0,0,.5);
	}
	
	.show-all-screens {
	  display: flex;
	  flex-direction: column;
	  align-items: center;
	  justify-content: center;
	  gap: 8px;
	  background: rgba(255,255,255,.05);
	  border: 1px dashed rgba(255,255,255,.2);
	  border-radius: 14px;
	  color: #cfd2ff;
	  text-decoration: none;
	  transition: background .2s ease, transform .2s ease;
	}
	
	.show-all-screens:hover {
	  background: rgba(255,255,255,.1);
	  transform: scale(1.03);
	}
	
	.show-all-screens span:first-child {
	  font-size: 42px;
	  opacity: .8;
	}
	</style>