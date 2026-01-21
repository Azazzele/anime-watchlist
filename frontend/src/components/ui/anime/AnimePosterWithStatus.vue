<script setup lang="ts">
	import { ref } from 'vue'
	
	defineProps<{
		cover?: string
	}>()
	
	defineEmits(['open-poster'])
	
	type Status = 'watching' | 'planned' | 'completed' | 'paused' | 'dropped' | null
	const userStatus = ref<Status>(null)
	const menuOpen = ref(false)
	
	const toggleMenu = () => { menuOpen.value = !menuOpen.value }
	
	const setStatus = (status: Status) => {
	  userStatus.value = status
	  menuOpen.value = false
	}
	
	const userStatusLabel = (status: Status) => {
	  switch (status) {
		case 'watching':   return 'Смотрю'
		case 'planned':    return 'В планах'
		case 'completed':  return 'Просмотрено'
		case 'paused':     return 'Отложено'
		case 'dropped':    return 'Заброшено'
		default:           return 'Выбрать статус'
	  }
	}
	</script>
	
	<template>
	  <div class="poster-wrap">
		<img
		  :src="cover"
		  class="poster"
		  alt="Poster"
		  @click="$emit('open-poster')"
		/>
	
		<div class="watch-status status-dropdown">
		  <button
			class="status-btn"
			:class="userStatus"
			@click.stop="toggleMenu"
		  >
			{{ userStatusLabel(userStatus) }}
		  </button>
	
		  <div v-if="menuOpen" class="status-menu">
			<button @click="setStatus('watching')">Смотрю</button>
			<button @click="setStatus('planned')">В планах</button>
			<button @click="setStatus('completed')">Просмотрено</button>
			<button @click="setStatus('paused')">Отложено</button>
			<button @click="setStatus('dropped')">Заброшено</button>
			<button @click="setStatus(null)">Убрать статус</button>
		  </div>
		</div>
	  </div>
	</template>
	
	<style scoped>
	.poster-wrap { position: relative; }
	
	.poster {
	  width: 100%;
	  border-radius: 16px;
	  box-shadow: 0 20px 60px rgba(0,0,0,.6);
	  cursor: zoom-in;
	  position: relative;
	  z-index: 1;
	}
	
	.watch-status { position: relative; margin-top: 15px; }
	
	.status-btn {
	  width: 100%;
	  padding: 10px 18px;
	  border-radius: 5px;
	  background: rgba(255,255,255,.06);
	  border: none;
	  cursor: pointer;
	  font-size: .9rem;
	  z-index: 3;
	}
	
	.status-btn.watching   { background: linear-gradient(135deg, #22c55e, #16a34a); box-shadow: 0 0 0 1px rgba(34,197,94,.35); }
	.status-btn.planned    { background: linear-gradient(135deg, #3b82f6, #2563eb); box-shadow: 0 0 0 1px rgba(59,130,246,.35); }
	.status-btn.completed  { background: linear-gradient(135deg, #a855f7, #7c3aed); box-shadow: 0 0 0 1px rgba(168,85,247,.35); }
	.status-btn.paused     { background: linear-gradient(135deg, #f59e0b, #d97706); box-shadow: 0 0 0 1px rgba(245,158,11,.35); }
	.status-btn.dropped    { background: linear-gradient(135deg, #ef4444, #dc2626); box-shadow: 0 0 0 1px rgba(239,68,68,.35); }
	
	.status-menu {
	  position: absolute;
	  width: 100%;
	  background: rgba(20, 22, 40, 0.96);
	  backdrop-filter: blur(12px);
	  padding: 10px;
	  display: flex;
	  flex-direction: column;
	  gap: 6px;
	  z-index: 10;
	  border-radius: 8px;
	}
	
	.status-menu button {
	  width: 100%;
	  background: transparent;
	  border: none;
	  padding: 8px 14px;
	  text-align: left;
	  color: #e6e6eb;
	  cursor: pointer;
	}
	
	.status-menu button:hover {
	  background: rgba(255,255,255,.08);
	}
	</style>