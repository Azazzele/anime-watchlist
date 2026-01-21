<script setup lang="ts">
	import { ref, computed } from 'vue'
	import type { Media } from '../../../types/type'
	
	const props = defineProps<{
	  anime: Media | null | undefined
	}>()
	
	const descriptionLang = ref<'ru' | 'en'>('ru')
	
	const activeDescription = computed(() => {
	  if (!props.anime) return 'Описание отсутствует'
	
	  if (descriptionLang.value === 'ru' && props.anime.descriptionRu) {
		return props.anime.descriptionRu
	  }
	
	  return props.anime.description || 'Описание отсутствует'
	})
	
	const canToggle = computed(() => Boolean(props.anime?.descriptionRu))
	
	const toggleDescriptionLang = () => {
	  if (!canToggle.value) return
	  descriptionLang.value = descriptionLang.value === 'ru' ? 'en' : 'ru'
	}
	</script>
	
	
	<template>
	  <div class="description-wrapper">
		<div class="description-header">
		  <h2 class='title_header'>Описание</h2>
	
		  <button
			class="lang-toggle"
			:disabled="!canToggle"
			@click="toggleDescriptionLang"
			:title="descriptionLang === 'ru'
				? 'Показать на английском'
				: 'Показать на русском'"
			>
			<span class="material-symbols-outlined">
			  {{ descriptionLang === 'ru' ? 'translate' : 'language' }}
			</span>
			<span class="lang-label">{{ descriptionLang.toUpperCase() }}</span>
		  </button>
		</div>
	
		<div class="description" v-html="activeDescription" />
	  </div>
	</template>
	
	<style scoped>
	.description-wrapper {
	  width: 1200px;
	  margin: 4em auto;
	}
	
	.description-header {
	  display: flex;
	  align-items: center;
	  justify-content: space-between;
	  margin-bottom: 14px;
	}
	
	.lang-toggle {
	  display: flex;
	  align-items: center;
	  gap: 6px;
	  padding: 6px 12px;
	  border-radius: 999px;
	  background: rgba(255,255,255,.06);
	  border: 1px solid rgba(255,255,255,.1);
	  color: #cfd2ff;
	  cursor: pointer;
	  font-size: .8rem;
	}
	
	.lang-toggle:hover:not(:disabled) {
	  background: rgba(255,255,255,.12);
	}
	
	.lang-toggle:disabled {
	  opacity: .4;
	  cursor: not-allowed;
	}
	
	.lang-label {
	  font-weight: 500;
	  letter-spacing: .5px;
	}
	
	.description {
	  margin-top: 8px;
	  line-height: 1.75;
	  color: #d8d9e6;
	}
	</style>