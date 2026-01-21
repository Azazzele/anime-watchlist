<script setup lang="ts">
	import { computed, ref } from 'vue'
	import type { Media } from '../../types/type'
	
	type RelationEdge = NonNullable<
	  NonNullable<Media['relations']>['edges']
	>[number]
	
	const props = defineProps<{
	  edges: RelationEdge[]
	}>()
	
	const expanded = ref(false)
	
	const sortedItems = computed(() =>
	  [...props.edges].sort((a, b) => {
		const yearA = a.node.startDate?.year ?? 9999
		const yearB = b.node.startDate?.year ?? 9999
		return yearA - yearB
	  })
	)
	
	const visibleItems = computed(() =>
	  expanded.value ? sortedItems.value : sortedItems.value.slice(0, 5)
	)
	
	const hasMore = computed(() => sortedItems.value.length > 5)
	
	/** map AniList type → route */
	const routeTypeMap: Record<string, string> = {
	  ANIME: 'anime',
	  MANGA: 'manga',
	  NOVEL: 'ranobe'
	}
	
	const getRoute = (edge: RelationEdge) => {
	  const type = routeTypeMap[edge.node.type ?? 'ANIME'] ?? 'anime'
	  return `/${type}/${edge.node.id}`
	}
	</script>
	
	<template>
	  <section class="relations-section">
		<h2 class="section-title">Связанное</h2>
	
		<div class="table-container">
		  <table class="relations-table">
			<thead>
			  <tr>
				<th>Постер</th>
				<th>Название</th>
				<th>Формат</th>
				<th>Тип связи</th>
				<th>Год</th>
			  </tr>
			</thead>
	
			<tbody>
			  <tr
				v-for="rel in visibleItems"
				:key="rel.node.id"
				class="table-row"
			  >
				<td class="poster-cell">
				  <img
					v-if="rel.node.coverImage?.large"
					:src="rel.node.coverImage.large"
					class="poster-img"
				  />
				  <div v-else class="poster-placeholder">Нет</div>
				</td>
	
				<td class="title-cell">
				  <router-link
					:to="getRoute(rel)"
					class="row-link"
				  >
					{{
					  rel.node.title?.romaji
					  || rel.node.title?.english
					  || 'Без названия'
					}}
				  </router-link>
				</td>
	
				<td class="format-cell">
				  {{ rel.node.format || '—' }}
				</td>
	
				<td class="type-cell">
				  <span class="badge">
					{{ rel.relationType || '?' }}
				  </span>
				</td>
	
				<td class="year-cell">
				  {{ rel.node.startDate?.year || '—' }}
				</td>
			  </tr>
			</tbody>
		  </table>
		</div>
	
		<div v-if="hasMore" class="show-more-wrap">
		  <button class="show-more-btn" @click="expanded = !expanded">
			{{ expanded ? 'Скрыть' : `Показать все (${sortedItems.length})` }}
		  </button>
		</div>
	  </section>
	</template>
	
	
	<style scoped>
	.relations-section {
	  margin: 40px 0;
	}
	
	.section-title {
	  font-size: 1.3rem;
	  font-weight: 600;
	  color: #e2e8f0;
	  margin-bottom: 16px;
	}
	
	.table-container {
	  overflow-x: auto;
	  border-radius: 12px;
	  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}
	
	.relations-table {
	  width: 100%;
	  border-collapse: collapse;
	  min-width: 720px;
	  background: rgba(30, 35, 55, 0.4);
	}
	
	.relations-table th,
	.relations-table td {
	  padding: 12px 16px;
	  text-align: left;
	  border-bottom: 1px solid #334155;
	}
	
	.relations-table th {
	  font-size: 0.78rem;
	  font-weight: 600;
	  color: #94a3b8;
	  text-transform: uppercase;
	  letter-spacing: 0.04em;
	  background: rgba(20, 25, 45, 0.6);
	}
	
	.poster-cell {
	  width: 100px;
	  padding: 12px 8px;
	}
	
	.poster-img {
	  width: 80px;
	  aspect-ratio: 2 / 3;
	  object-fit: cover;
	  border-radius: 8px;
	  box-shadow: 0 2px 8px rgba(0,0,0,0.4);
	}
	
	.poster-placeholder {
	  width: 80px;
	  height: 120px;
	  background: #1e293b;
	  border-radius: 8px;
	  display: flex;
	  align-items: center;
	  justify-content: center;
	  color: #64748b;
	  font-size: 0.8rem;
	}
	
	.title-cell {
	  font-size: 0.92rem;
	  color: #f1f5f9;
	  font-weight: 500;
	  max-width: 260px;
	}
	
	.row-link {
	  color: #e2e8f0;
	  text-decoration: none;
	  transition: color 0.15s ease;
	}
	
	.row-link:hover {
	  color: #c7d2fe;
	}
	
	.format-cell,
	.year-cell {
	  font-size: 0.85rem;
	  color: #cbd5e1;
	}
	
	.type-cell .badge {
	  padding: 4px 10px;
	  border-radius: 999px;
	  font-size: 0.68rem;
	  font-weight: 600;
	  background: rgba(99, 102, 241, 0.2);
	  color: #c7d2fe;
	  border: 1px solid rgba(99, 102, 241, 0.4);
	}
	
	.show-more-wrap {
	  margin-top: 16px;
	  text-align: center;
	}
	
	.show-more-btn {
	  background: transparent;
	  border: 1px solid rgba(165, 180, 252, 0.3);
	  color: #c7d2fe;
	  padding: 8px 18px;
	  border-radius: 8px;
	  font-size: 0.85rem;
	  cursor: pointer;
	  transition: all 0.2s ease;
	}
	
	.show-more-btn:hover {
	  background: rgba(165, 180, 252, 0.1);
	  border-color: rgba(165, 180, 252, 0.5);
	}
	
	/* Адаптив */
	@media (max-width: 768px) {
	  .relations-table th,
	  .relations-table td {
		padding: 10px 12px;
	  }
	  .poster-img {
		width: 70px;
	  }
	}
	</style>