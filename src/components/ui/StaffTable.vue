<script setup lang="ts">
	import { computed } from 'vue'
	import { useRoute } from 'vue-router'
	
	interface StaffEdge {
	  role: string
	  node: {
		id: number
		name?: { full?: string }
		image?: { large?: string }
	  }
	}
	
	const props = defineProps<{
	  edges: StaffEdge[]
	  limit?: number
	}>()
	
	const route = useRoute()
	
	/* ключевые роли */
	const directorKeywords = [
	  'director',
	  'chief director',
	  'series director',
	  'episode director',
	  'animation director'
	]
	
	const creatorKeywords = [
	  'original creator',
	  'original story',
	  'original manga',
	  'original character',
	  'story & art',
	  'manga',
	  'creator'
	]
	
	const isDirector = (role: string) =>
	  directorKeywords.some(k => role.toLowerCase().includes(k))
	
	const isCreator = (role: string) =>
	  creatorKeywords.some(k => role.toLowerCase().includes(k))
	
	const filteredStaff = computed(() => {
	  const all = props.edges ?? []
	
	  const directors = all
		.filter(e => isDirector(e.role))
		.sort((a, b) =>
		  a.role.toLowerCase().includes('chief') ? -1 : 1
		)
	
	  const creators = all.filter(
		e => isCreator(e.role) && !isDirector(e.role)
	  )
	
	  const seen = new Set<number>()
	  return [...directors, ...creators].filter(e => {
		if (seen.has(e.node.id)) return false
		seen.add(e.node.id)
		return true
	  })
	})
	
	const limit = computed(() => props.limit ?? 6)
	
	const displayed = computed(() =>
	  filteredStaff.value.slice(0, limit.value)
	)
	
	const hasMore = computed(() =>
	  filteredStaff.value.length > limit.value
	)
	</script>
	
	<template>
	  <section class="staff-section">
		<h2 class="section-title">Ключевой персонал</h2>
	
		<div v-if="filteredStaff.length === 0" class="empty-message">
		  Нет данных о режиссёрах и авторах оригинала
		</div>
	
		<div v-else class="table-container">
		  <table class="staff-table">
			<thead>
			  <tr>
				<th>Фото</th>
				<th>Имя</th>
				<th>Роль</th>
			  </tr>
			</thead>
	
			<tbody>
			  <tr
				v-for="person in displayed"
				:key="person.node.id"
				class="table-row"
			  >
				<td class="photo-cell">
				  <router-link :to="`/staff/${person.node.id}`">
					<img
					  v-if="person.node.image?.large"
					  :src="person.node.image.large"
					  class="staff-photo"
					/>
					<div v-else class="photo-placeholder">—</div>
				  </router-link>
				</td>
	
				<td class="name-cell">
				  <router-link
					:to="`/staff/${person.node.id}`"
					class="row-link"
				  >
					{{ person.node.name?.full || '???' }}
				  </router-link>
				</td>
	
				<td class="role-cell">
				  <span class="role-badge">
					{{ person.role }}
				  </span>
				</td>
			  </tr>
			</tbody>
		  </table>
		</div>
	
		<div v-if="hasMore" class="show-more">
		  <router-link
			:to="`${route.path}/staff`"
			class="show-more-btn"
		  >
			Ещё {{ filteredStaff.length - limit }} человек →
		  </router-link>
		</div>
	  </section>
	</template>
	
	
<style scoped>
.role-badge {
  padding: 4px 10px;
  border-radius: 999px;
  font-size: 0.82rem;
  font-weight: 500;
  background: rgba(99, 102, 241, 0.15);
  color: #c7d2fe;
  border: 1px solid rgba(99, 102, 241, 0.3);
}

.empty-message {
  padding: 20px;
  text-align: center;
  color: #94a3b8;
  font-style: italic;
}

.show-more {
  margin-top: 16px;
  text-align: center;
}

.show-more-btn {
  color: #c7d2fe;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.show-more-btn:hover {
  color: #a5b4fc;
}
	.staff-section {
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
	
	.staff-table {
	  width: 100%;
	  border-collapse: collapse;
	  min-width: 600px;
	  background: rgba(30, 35, 55, 0.4);
	}
	
	.staff-table th,
	.staff-table td {
	  padding: 12px 16px;
	  text-align: left;
	  border-bottom: 1px solid #334155;
	}
	
	.staff-table th {
	  font-size: 0.78rem;
	  font-weight: 600;
	  color: #94a3b8;
	  text-transform: uppercase;
	  letter-spacing: 0.04em;
	  background: rgba(20, 25, 45, 0.6);
	}
	
	.photo-cell {
	  width: 80px;
	  padding: 12px 8px;
	}
	
	.staff-photo {
	  width: 64px;
	  height: 64px;
	  object-fit: cover;
	  border-radius: 50%;
	  border: 2px solid rgba(165, 180, 252, 0.2);
	}
	
	.photo-placeholder {
	  width: 64px;
	  height: 64px;
	  background: #1e293b;
	  border-radius: 50%;
	  display: flex;
	  align-items: center;
	  justify-content: center;
	  color: #64748b;
	  font-size: 0.8rem;
	}
	
	.name-cell,
	.role-cell {
	  font-size: 0.92rem;
	  color: #f1f5f9;
	}
	
	.row-link {
	  color: #e2e8f0;
	  text-decoration: none;
	  transition: color 0.15s ease;
	}
	
	.row-link:hover {
	  color: #c7d2fe;
	}
	
	.role-badge {
	  padding: 4px 10px;
	  border-radius: 999px;
	  font-size: 0.82rem;
	  font-weight: 500;
	  background: rgba(99, 102, 241, 0.15);
	  color: #c7d2fe;
	  border: 1px solid rgba(99, 102, 241, 0.3);
	}
	
	.empty-message {
	  padding: 20px;
	  text-align: center;
	  color: #94a3b8;
	  font-style: italic;
	}
	
	.show-more {
	  margin-top: 16px;
	  text-align: center;
	}
	
	.show-more-btn {
	  color: #c7d2fe;
	  text-decoration: none;
	  font-weight: 500;
	  transition: color 0.2s;
	}
	
	.show-more-btn:hover {
	  color: #a5b4fc;
	}
	
	@media (max-width: 768px) {
	  .staff-table th,
	  .staff-table td {
		padding: 10px 12px;
	  }
	
	  .staff-photo {
		width: 56px;
		height: 56px;
	  }
	}
	</style>
	