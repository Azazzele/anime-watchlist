<script setup lang="ts">
	import { ref, watch } from 'vue'
	
	/* =======================
	   PROPS
	======================= */
	const props = defineProps<{
	  staffId: number
	}>()
	
	/* =======================
	   STATE
	======================= */
	const staff = ref<any>(null)
	const loading = ref(true)
	const error = ref<string | null>(null)
	
	/* =======================
	   LOAD STAFF
	======================= */
	const loadStaff = async () => {
	  loading.value = true
	  error.value = null
	
	  if (!props.staffId || props.staffId <= 0) {
		error.value = 'Некорректный ID сэйю'
		loading.value = false
		return
	  }
	
	  try {
		// временная заглушка
		staff.value = {
		  id: props.staffId,
		  name: `Сэйю #${props.staffId}`,
		  image: null,
		  description: 'Страница в разработке',
		}
	  } catch (e) {
		console.error(e)
		error.value = 'Ошибка загрузки сэйю'
		staff.value = null
	  } finally {
		loading.value = false
	  }
	}
	
	watch(
	  () => props.staffId,
	  loadStaff,
	  { immediate: true }
	)
	</script>
	
	<template>
	  <div class="staff-page">
		<div v-if="loading" class="loading">Загрузка…</div>
	
		<div v-else-if="error" class="error">{{ error }}</div>
	
		<div v-else-if="staff" class="content">
		  <div class="avatar-wrap">
			<img
			  v-if="staff.image"
			  :src="staff.image"
			  alt="Сэйю"
			  class="avatar"
			/>
			<div v-else class="avatar-placeholder">Нет фото</div>
		  </div>
	
		  <div class="info">
			<h1>{{ staff.name }}</h1>
			<p class="desc">{{ staff.description }}</p>
		  </div>
		</div>
	  </div>
	</template>
	
	<style scoped>
	.staff-page {
	  max-width: 900px;
	  margin: 0 auto;
	  padding: 40px 16px;
	  color: #e5e7eb;
	}
	
	.loading,
	.error {
	  text-align: center;
	  opacity: 0.7;
	}
	
	.content {
	  display: flex;
	  gap: 32px;
	}
	
	.avatar-wrap {
	  width: 240px;
	}
	
	.avatar {
	  width: 100%;
	  border-radius: 16px;
	  box-shadow: 0 20px 40px rgba(0,0,0,.5);
	}
	
	.avatar-placeholder {
	  width: 100%;
	  aspect-ratio: 3 / 4;
	  background: #111827;
	  border-radius: 16px;
	  display: flex;
	  align-items: center;
	  justify-content: center;
	  color: #64748b;
	}
	
	.info h1 {
	  font-size: 2rem;
	  margin-bottom: 12px;
	}
	
	.desc {
	  opacity: .85;
	  line-height: 1.7;
	}
	</style>
	