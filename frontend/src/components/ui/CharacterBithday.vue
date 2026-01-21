<script setup lang="ts">
	import { ref, onMounted } from 'vue'
	
	interface BirthdayCharacter {
	  id: number
	  name_full: string
	  image_large: string | null
	}
	
	const birthdays = ref<BirthdayCharacter[]>([])
	const loading = ref(true)
	const error = ref<string | null>(null)
	
	onMounted(async () => {
	  try {
		const res = await fetch('http://127.0.0.1:8000/characters/today-birthdays')
		if (!res.ok) throw new Error('Ошибка загрузки')
		birthdays.value = await res.json()
	  } catch (e) {
		error.value = 'Не удалось загрузить персонажей с ДР'
	  } finally {
		loading.value = false
	  }
	})
	</script>
	
	<template>
	  <section class="birthdays">
		<h2 class="title_header">Сегодня день рождения у персонажей</h2>
	
		<div v-if="loading" class="state">Загрузка...</div>
		<div v-else-if="error" class="state error">{{ error }}</div>
	
		<div v-else-if="birthdays.length === 0" class="state">
		  Сегодня никто из известных персонажей не празднует ДР 😔
		</div>
	
		<div v-else class="grid">
		  <article
			v-for="char in birthdays"
			:key="char.id"
			class="card"
		  >
			<router-link
			  :to="`/character/${char.id}`"
			  class="poster-link"
			>
			  <img
				v-if="char.image_large"
				:src="char.image_large"
				:alt="char.name_full"
			  />
			  <div v-else class="placeholder">Нет фото</div>
			</router-link>
	
			<h3 class="name">
			  <router-link
				:to="`/character/${char.id}`"
				class="name-link"
			  >
				{{ char.name_full }}
			  </router-link>
			</h3>
		  </article>
		</div>
	  </section>
	</template>
	
	<style scoped>
	.birthdays {
	  margin-top: 120px;
	}
	
	.title_header {
	  text-align: center;
	  font-size: 1.9rem;
	  margin-bottom: 32px;
	}
	
	.state {
	  text-align: center;
	  color: #94a3b8;
	  font-size: 1.05rem;
	}
	
	.error {
	  color: #ef4444;
	}
	
	.grid {
	  display: grid;
	  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
	  gap: 18px;
	  padding: 0 16px;
	}
	
	.card {
	  border-radius: 14px;
	  overflow: hidden;
	  background: #0f1117;
	  text-align: center;
	  transition: transform 0.2s ease;
	}
	
	.card:hover {
	  transform: translateY(-6px);
	}
	
	.poster-link {
	  display: block;
	}
	
	.card img,
	.placeholder {
	  width: 100%;
	  aspect-ratio: 3 / 4;
	  object-fit: cover;
	  background: #1a1d2a;
	}
	
	.placeholder {
	  display: flex;
	  align-items: center;
	  justify-content: center;
	  color: #64748b;
	  font-size: 0.85rem;
	}
	
	.name {
	  padding: 10px 8px 14px;
	}
	
	.name-link {
	  color: #e5e7eb;
	  text-decoration: none;
	  font-size: 0.95rem;
	  font-weight: 500;
	}
	
	.name-link:hover {
	  color: #64b5f6;
	}
	</style>
	