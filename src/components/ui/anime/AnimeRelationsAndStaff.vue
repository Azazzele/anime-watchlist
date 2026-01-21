<script setup lang="ts">
	import { computed } from 'vue'
	import type { Media } from '../../../types/type'
	
	import RelationsRow from '../RelationsTimeline.vue'
	import StaffTable from '../StaffTable.vue'
	
	const props = defineProps<{
	  anime: Media | null | undefined
	}>()
	
	const relationsEdges = computed(() => props.anime?.relations?.edges ?? [])
	const staffEdges = computed(() => props.anime?.staff?.edges ?? [])
	</script>
	
	<template>
	  <div class="relations-layout">
		<!-- Связанные тайтлы -->
		<RelationsRow
		  v-if="relationsEdges.length > 0"
		  :edges="relationsEdges"
		/>
	
		<!-- Персонал -->
		<StaffTable
		  v-if="staffEdges.length > 0"
		  :edges="staffEdges"
		  :limit="10"
		/>
	  </div>
	</template>
	
	<style scoped>
	.relations-layout {
	  display: grid;
	  grid-template-columns: 1fr 1fr;
	  gap: 32px;
	  max-width: 1780px;
	  margin: 60px auto;
	  padding: 0 32px;
	}
	
	@media (max-width: 1024px) {
	  .relations-layout {
		grid-template-columns: 1fr;
		gap: 48px;
	  }
	}
	</style>
	