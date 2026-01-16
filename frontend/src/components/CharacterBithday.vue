<script setup lang="ts">
	import { ref, onMounted } from 'vue'
	
	
	const birthdays = ref([])
	const loading = ref(true)
	const error = ref<string | null>(null)
	
	onMounted(async () => {
	  try {
		const res = await fetch('http://127.0.0.1:8000/characters/today-birthdays')
		if (!res.ok) {
		  throw new Error(`HTTP ${res.status}: ${await res.text()}`)
		}
		birthdays.value = await res.json()
	  } catch (e) {
		error.value = 'Не удалось загрузить персонажей с ДР'
		console.error('Ошибка:', e)
	  } finally {
		loading.value = false
	  }
	})
	</script>
	
	<template>
	  <section class="birthdays">
		<h2 class="title_header">Сегодня день рождения у персонажей</h2>
	
		<div v-if="loading">Загрузка...</div>
		<div v-else-if="error" class="error">{{ error }}</div>
		<div v-else-if="birthdays.length === 0">
		  Сегодня никто из известных персонажей не празднует ДР 😔
		</div>
		<div v-else class="grid">
		  <article v-for="char in birthdays" :key="char.id" class="card">
			<a
			  :href="`https://anilist.co/character/${char.id}`"
			  target="_blank"
			  rel="noopener noreferrer"
			  class="poster-link"
			>
			  <img
				v-if="char.image_large"
				:src="char.image_large"
				:alt="char.name_full"
				loading="lazy"
			  />
			  <div v-else class="placeholder">Нет фото</div>
			</a>
	
			<h3>
			  <a
				:href="`https://anilist.co/character/${char.id}`"
				target="_blank"
				rel="noopener noreferrer"
				class="name-link"
			  >
				{{ char.name_full }}
			  </a>
			</h3>
		  </article>
		</div>
	  </section>
	</template>
	
	<style scoped>
	.birthdays {
	  margin-top: 120px;
	}
	
	.grid {
	  display: grid;
	  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
	  gap: 14px;
	  padding: 0 16px;
	}
	
	.card {
	  border-radius: 12px;
	  overflow: hidden;
	  text-align: center;
	  background: #0f1117;
	  transition: transform 0.2s ease;
	}
	
	.card:hover {
	  transform: translateY(-6px);
	}
	
	.poster-link {
	  display: block;
	  text-decoration: none;
	}
	
	.card img {
	  width: 220px;
	  height:320px;
	  aspect-ratio: 3/4;
	  object-fit: cover;
	}
	
	.placeholder {
	  width: 220px;
	  aspect-ratio: 3/4;
	  background: #1a1d2a;
	  display: flex;
	  align-items: center;
	  justify-content: center;
	  color: #555;
	  font-size: 0.8rem;
	}
	
	.name-link {
	  color: #e0e0e0;
	  text-decoration: none;
	  font-size: 0.95rem;
	  font-weight: 500;
	}
	
	.name-link:hover {
	  color: #64b5f6;
	}
	
	.card p a {
	  color: #aaa;
	  text-decoration: none;
	  font-size: 0.8rem;
	}
	
	.card p a:hover {
	  color: #64b5f6;
	}
	
	.date {
	  display: block;
	  margin-top: 6px;
	  font-size: 0.75rem;
	  color: #64dd17;
	}
	</style>