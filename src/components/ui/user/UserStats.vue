<script setup lang="ts">
	import type { UserStatistics } from '../../../types/user'
	
	defineProps<{
	  stats: UserStatistics
	}>()
	</script>

<template>
	<div class="section stats">
	  <h2 class="section-title">Статистика</h2>
	  <div class="stats-grid">
		<div v-if="stats.anime" class="stat-card anime">
		  <h3>Аниме</h3>
		  <div class="stat-row">
			<div class="stat-item">
			  <span class="value">{{ stats.anime.count || 0 }}</span>
			  <span class="label">Просмотрено</span>
			</div>
			<div class="stat-item">
			  <span class="value">{{ stats.anime.meanScore?.toFixed(2) || '—' }}</span>
			  <span class="label">Средний балл</span>
			</div>
			<div class="stat-item">
			  <span class="value">{{ stats.anime.minutesWatched?.toLocaleString() || '—' }}</span>
			  <span class="label">Минут</span>
			</div>
		  </div>
		</div>
		<div v-if="stats.manga" class="stat-card manga">
		  <h3>Манга</h3>
		  <div class="stat-row">
			<div class="stat-item">
			  <span class="value">{{ stats.manga.count || 0 }}</span>
			  <span class="label">Прочитано</span>
			</div>
			<div class="stat-item">
			  <span class="value">{{ stats.manga.meanScore?.toFixed(2) || '—' }}</span>
			  <span class="label">Средний балл</span>
			</div>
		  </div>
		</div>
	  </div>
	</div>
  </template>
  
  <style scoped>
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
  
  .stats-grid {
	display: grid;
	grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
	gap: 1.5rem;
  }
  
  .stat-card {
	background: rgba(99, 102, 241, 0.05);
	border-radius: 12px;
	padding: 1.5rem;
  }
  
  .stat-card h3 {
	font-size: 1.3rem;
	margin-bottom: 1rem;
	color: #6366f1;
  }
  
  .stat-row {
	display: flex;
	flex-wrap: wrap;
	gap: 1.2rem;
	justify-content: center;
  }
  
  .stat-item {
	text-align: center;
	min-width: 120px;
  }
  
  .value {
	font-size: 2rem;
	font-weight: bold;
	color: #6366f1;
	display: block;
  }
  
  .label {
	font-size: 0.95rem;
	color: #6c757d;
	display: block;
  }
  </style>