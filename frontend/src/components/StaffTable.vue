<script setup lang="ts">
	import { computed } from 'vue'
	import { useRouter } from 'vue-router'
	
	interface StaffEdge {
		role: string
		node: {
			id: number
			name: {
			full?: string
			native?: string
			}
			image?: {
			large?: string
			}
		}
		}
	
	const props = defineProps<{
	  staff: { edges: StaffEdge[] }
	}>()
	
	const items = computed(() => props.staff?.edges?.slice(0, 3) ?? [])
</script>
	
	

	<template>
		<section class="relations-table">
		  <h2 class="relations-table__title">Производственный персонал</h2>
	  
		  <div class="table-container">
			<table class="relations-table__table">
			  <thead>
				<tr>
				  <th>Фото</th>
				  <th>Имя</th>
				  <th>Роль</th>
				</tr>
			  </thead>
	  
			  <tbody>
				<tr
					v-for="person in items"
					:key="person.node.id"
					class="table-row-link"
				>
					<td class="poster-cell">
					<router-link :to="`/staff/${person.node.id}`">
						<img
						:src="person.node.image?.large"
						class="poster-img"
						/>
					</router-link>
					</td>

					<td class="title-cell">
					<router-link
						:to="`/staff/${person.node.id}`"
						class="row-link"
					>
						{{ person.node.name.full }}
					</router-link>
					</td>

					<td class="role-cell">
					<router-link
						:to="`/staff/${person.node.id}`"
						class="row-link"
					>
						{{ person.role }}
					</router-link>
					</td>
				</tr>
			</tbody>

			</table>
		  </div>
		</section>
	  </template>
	  
	  

<style>
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
</style>