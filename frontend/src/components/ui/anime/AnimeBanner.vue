<script setup lang="ts">
	defineProps<{
	  background?: string
	}>()
	</script>
	
	<template>
	  <div class="banner" :style="{ backgroundImage: `url(${background || ''})` }" />
	</template>
	
	<style scoped>
	.banner {
	  height: 320px;
	  background-size:contain;
	  background-position: center;
	}
	</style>