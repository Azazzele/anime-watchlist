<script setup lang="ts">

	interface VoiceActor {
	  id: number
	  name: string
	  image?: string | null 
	}
	
	defineProps<{
	  actor: VoiceActor | null | undefined
	}>()
	</script>
	
	<template>
	  <div
		v-if="actor"
		:to="`/staff/${actor.id}`"
		class="va-card"
	  >
		<!-- Фото или плейсхолдер -->
		<div class="va-image-wrap">
		  <img
			v-if="actor.image"
			:src="actor.image"
			class="va-image"
			alt="Сэйю"
			loading="lazy"
		  />
		  <div v-else class="va-placeholder">
			Нет фото
		  </div>
		</div>
	
		<!-- Имя -->
		<span class="va-name">
		  {{ actor.name || 'Неизвестно' }}
		</span>
	
		<!-- Лейбл -->
		<span class="va-label">Сэйю</span>
	</div>
	
	  <!-- Если actor не передан -->
	  <div v-else class="va-card empty">
		<span class="va-placeholder-text">Сэйю не найден</span>
	  </div>
	</template>
	
	<style scoped>
	.va-card {
	  display: flex;
	  flex-direction: column;
	  align-items: center;
	  gap: 8px;
	  text-decoration: none;
	  color: inherit;
	  background: #0b0d14;
	  border-radius: 14px;
	  padding: 12px 10px;
	  width: 160px;
	  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
	  transition: transform 0.2s ease, box-shadow 0.2s ease;
	}
	
	.va-card:hover {
	  transform: translateY(-4px);
	  box-shadow: 0 14px 40px rgba(0, 0, 0, 0.5);
	}
	
	.va-card.empty {
	  justify-content: center;
	  min-height: 220px;
	  opacity: 0.6;
	}
	
	.va-image-wrap {
	  width: 100%;
	  position: relative;
	}
	
	.va-image {
	  width: 100%;
	  aspect-ratio: 3 / 4;
	  object-fit: cover;
	  border-radius: 10px;
	  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
	}
	
	.va-placeholder {
	  width: 100%;
	  aspect-ratio: 3 / 4;
	  border-radius: 10px;
	  background: #111827;
	  display: flex;
	  align-items: center;
	  justify-content: center;
	  color: #64748b;
	  font-size: 0.9rem;
	  font-weight: 500;
	}
	
	.va-placeholder-text {
	  font-size: 0.9rem;
	  color: #64748b;
	}
	
	.va-name {
	  font-size: 0.88rem;
	  font-weight: 600;
	  text-align: center;
	  line-height: 1.2;
	  color: #e5e7eb;
	  max-width: 100%;
	  overflow: hidden;
	  text-overflow: ellipsis;
	  display: -webkit-box;
	  -webkit-line-clamp: 2;
	  -webkit-box-orient: vertical;
	}
	
	.va-label {
	  font-size: 0.72rem;
	  opacity: 0.65;
	  color: #c7d2fe;
	  letter-spacing: 0.5px;
	}
	</style>