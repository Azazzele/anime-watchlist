<script setup lang="ts">
	import { computed } from 'vue'
	import { useRoute } from 'vue-router'
	import { useUserProfile } from '../../composables/useUserProfile'
	import type { UserProfile } from '../../types/user'
	
	// Компоненты (можно вынести в отдельные файлы)
	import UserProfileHeader from '../../components/ui/user/UserProfileHeader.vue'
	import UserStats from '../../components/ui/user/UserStats.vue'
	import FavouritesSection from '../../components/ui/user/FavouritesSection.vue'
	
	const route = useRoute()
	const username = computed(() => route.params.username as string)
	
	const { user, isLoading, error } = useUserProfile(username.value)
</script>
<template>
	<div class="user-profile-page">
	  <div v-if="isLoading" class="loading">
		<div class="spinner"></div>
		<p>Загружаем профиль...</p>
	  </div>
  
	  <div v-else-if="error || !user" class="error">
		<h2>Профиль не найден</h2>
		<p>{{ error?.message || 'Пользователь не существует или произошла ошибка' }}</p>
	  </div>
  
	  <div v-else>
		<!-- 1. Заголовок с баннером и аватаром -->
		<UserProfileHeader :user="user" />
  
		<!-- Основной контент -->
		<div class="container">
		  <!-- 2. Статистика -->
		  <UserStats v-if="user.statistics" :stats="user.statistics" />
  
		  <!-- 3. О себе -->
		  <div v-if="user.about" class="section about">
			<h2 class="section-title">О себе</h2>
			<p class="about-text" v-html="user.about.replace(/\n/g, '<br>')"></p>
		  </div>
  
		  <!-- 4. Избранное (аниме, манга, персонажи, персонал) -->
		  <FavouritesSection
			v-if="user.favourites?.anime?.length"
			title="Любимые аниме"
			:items="user.favourites.anime"
			type="anime"
		  />
  
		  <FavouritesSection
			v-if="user.favourites?.manga?.length"
			title="Любимая манга"
			:items="user.favourites.manga"
			type="manga"
		  />
  
		  <FavouritesSection
			v-if="user.favourites?.characters?.length"
			title="Любимые персонажи"
			:items="user.favourites.characters"
			type="character"
		  />
  
		  <FavouritesSection
			v-if="user.favourites?.staff?.length"
			title="Любимые сэйю / авторы"
			:items="user.favourites.staff"
			type="staff"
		  />
  
		  <!-- Футер -->
		  <div class="profile-footer">
			<p>
			  AniList:
			  <a :href="user.siteUrl" target="_blank" rel="noopener noreferrer">
				{{ user.siteUrl?.replace('https://anilist.co/user/', '') }}
			  </a>
			</p>
		  </div>
		</div>
	  </div>
	</div>
  </template>
  
  
  <style scoped>
  .user-profile-page {
	min-height: 100vh;
	background: #f8f9fa;
	color: #212529;
  }
  
  .container {
	max-width: 1200px;
	margin: 0 auto;
	padding: 0 1rem;
  }
  
  .section {
	background: white;
	border-radius: 12px;
	padding: 1.8rem;
	margin-bottom: 1.8rem;
	box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  }
  
  .section-title {
	font-size: 1.5rem;
	font-weight: bold;
	margin-bottom: 1.2rem;
	color: #6366f1;
  }
  
  .about-text {
	white-space: pre-wrap;
	line-height: 1.6;
  }
  
  .profile-footer {
	text-align: center;
	padding: 2rem 0;
	color: #6c757d;
	font-size: 0.95rem;
  }
  
  .loading, .error {
	height: 100vh;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
  }
  
  .spinner {
	width: 50px;
	height: 50px;
	border: 5px solid #e5e7eb;
	border-top: 5px solid #6366f1;
	border-radius: 50%;
	animation: spin 1s linear infinite;
	margin-bottom: 1rem;
  }
  
  @keyframes spin {
	0% { transform: rotate(0deg); }
	100% { transform: rotate(360deg); }
  }
  
  /* Тёмная тема по системным настройкам */
  @media (prefers-color-scheme: dark) {
	.user-profile-page {
	  background: #111827;
	  color: #f3f4f6;
	}
  
	.section {
	  background: #1f2937;
	  border: 1px solid #374151;
	}
  
	.profile-footer {
	  color: #9ca3af;
	}
  }
  </style>