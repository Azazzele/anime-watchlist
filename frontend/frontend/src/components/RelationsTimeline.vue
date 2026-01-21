<script setup lang="ts">
	import { computed, ref } from 'vue'
	
	interface Relation {
	  relationType: string
	  node: {
		id: number
		format?: string
		startDate?: { year?: number }
		title: {
		  romaji?: string
		  english?: string
		}
		coverImage?: {
		  large?: string
		}
	  }
	}
	
	const props = defineProps<{
	  relations: { edges: Relation[] }
	}>()
	
	const expanded = ref(false)
	
	const sortedItems = computed(() =>
	  [...props.relations.edges].sort(
		(a, b) =>
		  (a.node.startDate?.year ?? 9999) -
		  (b.node.startDate?.year ?? 9999)
	  )
	)
	
	const visibleItems = computed(() =>
	  expanded.value ? sortedItems.value : sortedItems.value.slice(0, 5)
	)
	</script>
	
		
		<template>
		<section class="relations-table">
			<h2 class="relations-table__title">Связанное</h2>
		
		
			<div class="table-container">
			<table class="relations-table__table">
				<thead>
				<tr>
					<th>Постер</th>
					<th>Название</th>
					<th>Формат</th>
					<th>Тип</th>
					<th>Год</th>
				</tr>
				</thead>
	<tbody>
		<tr
			v-for="rel in visibleItems"
			:key="rel.node.id"
			class="table-row-link"
		>
			<td class="poster-cell">
			<img
				:src="rel.node.coverImage?.large"
				alt=""
				class="poster-img"
			/>
			</td>

			<td class="title-cell">
			<router-link
				:to="`/anime/${rel.node.id}`"
				class="row-link"
			>
				{{ rel.node.title.romaji || rel.node.title.english }}
			</router-link>
			</td>

			<td class="format-cell">
			{{ rel.node.format || '—' }}
			</td>

			<td class="type-cell">
			<span class="badge">{{ rel.relationType }}</span>
			</td>

			<td class="year-cell">
			{{ rel.node.startDate?.year || '—' }}
			</td>
		</tr>
		</tbody>

		<!-- КНОПКА -->
		<div
		v-if="sortedItems.length > 5"
		class="show-more-wrap"
		>
		<button
			class="show-more-btn"
			@click="expanded = !expanded"
		>
			{{ expanded ? 'Скрыть' : 'Показать всё' }}
		</button>
		</div>

			</table>
			</div>
		</section>
		</template>
		
		<style scoped>
		.relations-table {
			margin: 40px 0;
			padding: 0 16px;
		}
		
		.relations-table__title {
			font-size: 1.3rem;
			font-weight: 600;
			color: #e2e8f0;
			margin-bottom: 16px;
			text-align: left;
		}
		
		.table-container {
			overflow-x: auto;
			border-radius: 12px;
			box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
		}
		
		.relations-table__table {
			width: 100%;
			border-collapse: collapse;
			min-width: 700px;
		}
		
		.relations-table__table th,
		.relations-table__table td {
			padding: 12px 16px;
			text-align: left;
			border-bottom: 1px solid #334155;
		}
		
		
		.relations-table__table th {
			font-size: 0.8rem;
			font-weight: 600;
			color: #94a3b8;
			text-transform: uppercase;
			letter-spacing: 0.05em;
		}
		
		.poster-cell {
			width: 120px;
			padding: 12px 0;
		}
		
		.poster-img {
			width: 100%;
			max-width: 100px;
			aspect-ratio: 2 / 3;
			object-fit: cover;
			border-radius: 8px;
			display: block;
		}
		
		.title-cell {
			font-size: 0.9rem;
			color: #f1f5f9;
			font-weight: 500;
			max-width: 200px;
		}
		
		.format-cell {
			font-size: 0.85rem;
			color: #cbd5e1;
			font-weight: 400;
			width: 100px;
		}
		
		.type-cell {
			width: 120px;
		}
		
		.badge {
			display: inline-block;
			padding: 4px 10px;
			border-radius: 20px;
			font-size: 0.65rem;
			font-weight: 600;
			text-transform: uppercase;
			letter-spacing: 0.05em;
			color: white;
		}
		
		
		.year-cell {
		width: 80px;
		font-size: 0.85rem;
		color: #94a3b8;
		}
		
		/* Адаптивность */
		@media (max-width: 768px) {
		.relations-table {
			padding: 0 8px;
		}
		
		.table-container {
			border-radius: 8px;
		}
		
		.relations-table__table th,
		.relations-table__table td {
			padding: 10px 12px;
			font-size: 0.85rem;
		}
		
		.poster-cell {
			width: 90px;
		}
		
		.poster-img {
			max-width: 80px;
		}
		
		.title-cell {
			max-width: 160px;
		}
		
		.format-cell,
		.type-cell,
		.year-cell {
			width: auto;
		}
		}
		.show-more-wrap {
			display: flex;
			justify-content: center;
			margin-top: 12px;
		}

		.show-more-btn {
			background: transparent;
			border: 1px solid rgba(255, 255, 255, 0.2);
			color: #e5e7eb;

			padding: 6px 14px;
			border-radius: 8px;

			font-size: 0.8rem;
			cursor: pointer;

			transition: all 0.2s ease;
		}

		.show-more-btn:hover {
			border-color: rgba(255, 255, 255, 0.4);
		}

		</style>
		