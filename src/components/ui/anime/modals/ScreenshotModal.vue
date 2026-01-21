<script setup lang="ts">
	defineProps<{ src: string }>()
	defineEmits(['close'])
	</script>
	
	<template>
	  <div class="media-overlay" @click.self="$emit('close')">
		<img
		  :src="src"
		  class="media-full"
		  alt="Full screenshot"
		  @click="$emit('close')"
		/>
	  </div>
	</template>
	
	<style scoped>
	.media-overlay {
	  position: fixed;
	  inset: 0;
	  background: rgba(0,0,0,.85);
	  display: flex;
	  align-items: center;
	  justify-content: center;
	  z-index: 1000;
	}
	
	.media-full {
	  max-width: 90%;
	  max-height: 90%;
	  border-radius: 18px;
	  cursor: zoom-out;
	}
	</style>