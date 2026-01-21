<script setup lang="ts">
	import { ref, computed } from 'vue'
	
	interface Review {
	  id: number
	  type: 'all' | 'positive' | 'neutral' | 'negative'
	  text: string
	}
	
	const reviews = ref<Review[]>([]) 
	
	const activeDiscussionTab = ref<'comments' | 'reviews'>('comments')
	const activeReviewFilter = ref<'all' | 'positive' | 'neutral' | 'negative'>('all')
	
	const setDiscussionTab = (tab: 'comments' | 'reviews') => {
	  activeDiscussionTab.value = tab
	}
	
	const reviewCounters = computed(() => ({
	  all: reviews.value.length,
	  positive: reviews.value.filter(r => r.type === 'positive').length,
	  neutral: reviews.value.filter(r => r.type === 'neutral').length,
	  negative: reviews.value.filter(r => r.type === 'negative').length,
	}))
	
	const setReviewFilter = (type: 'all' | 'positive' | 'neutral' | 'negative') => {
	  activeReviewFilter.value = type
	}
	</script>
	
	<template>
	  <section class="discussion-section">
		<div class="discussion-header">
		  <h2 class='title_header'>Обсуждение</h2>
	
		  <div class="discussion-tabs">
			<button
			  :class="{ active: activeDiscussionTab === 'comments' }"
			  @click="setDiscussionTab('comments')"
			>
			  Комментарии
			</button>
			<button
			  :class="{ active: activeDiscussionTab === 'reviews' }"
			  @click="setDiscussionTab('reviews')"
			>
			  Рецензии
			</button>
		  </div>
		</div>
	
		<div v-if="activeDiscussionTab === 'comments'" class="discussion-body">
		  <div class="empty-state">
			<span class="material-symbols-outlined">chat</span>
			<p>Комментариев пока нет</p>
			<button class="primary-btn">Написать комментарий</button>
		  </div>
		</div>
	
		<div v-else class="discussion-body">
		  <div class="reviews-filter-bar">
			<button
			  class="filter-pill"
			  :class="{ active: activeReviewFilter === 'all' }"
			  @click="setReviewFilter('all')"
			>
			  Все отзывы ({{ reviewCounters.all }})
			</button>
	
			<button
			  class="filter-pill positive"
			  :class="{ active: activeReviewFilter === 'positive' }"
			  :disabled="reviewCounters.positive === 0"
			  @click="setReviewFilter('positive')"
			>
			  <span class="material-symbols-outlined">sentiment_satisfied</span>
			  Положительные ({{ reviewCounters.positive }})
			</button>
	
			<button
			  class="filter-pill neutral"
			  :class="{ active: activeReviewFilter === 'neutral' }"
			  @click="setReviewFilter('neutral')"
			>
			  <span class="material-symbols-outlined">sentiment_neutral</span>
			  Нейтральные ({{ reviewCounters.neutral }})
			</button>
	
			<button
			  class="filter-pill negative"
			  :class="{ active: activeReviewFilter === 'negative' }"
			  @click="setReviewFilter('negative')"
			>
			  <span class="material-symbols-outlined">sentiment_dissatisfied</span>
			  Отрицательные ({{ reviewCounters.negative }})
			</button>
		  </div>
	
		  <div class="reviews-content">
			<p class="stub">
			  Активный фильтр: <strong>{{ activeReviewFilter }}</strong>
			</p>
			<!-- Здесь в будущем будет список рецензий -->
		  </div>
		</div>
	  </section>
	</template>
	
	<style scoped>
	.discussion-section {
	  max-width: 1480px;
	  margin: 80px auto;
	  padding: 0 32px;
	}
	
	.discussion-header {
	  display: flex;
	  align-items: center;
	  justify-content: space-between;
	  margin-bottom: 24px;
	}
	
	.discussion-header h2 {
	  font-size: 1.4rem;
	  font-weight: 600;
	}
	
	.discussion-tabs {
	  display: flex;
	  gap: 10px;
	}
	
	.discussion-tabs button {
	  padding: 8px 18px;
	  border-radius: 10px;
	  background: rgba(255,255,255,.06);
	  border: 1px solid rgba(255,255,255,.1);
	  color: #cfd2ff;
	  cursor: pointer;
	  font-size: .85rem;
	  transition: all .2s ease;
	}
	
	.discussion-tabs button.active {
	  color: white;
	  border-color: transparent;
	  background: linear-gradient(135deg, #6366f1, #4f46e5);
	}
	
	.discussion-body {
	  background: rgba(20, 22, 40, 0.6);
	  border-radius: 24px;
	  padding: 48px;
	  margin-top: 3em;
	  backdrop-filter: blur(18px);
	}
	
	.empty-state {
	  text-align: center;
	  color: #9ca3af;
	}
	
	.empty-state span {
	  font-size: 48px;
	  opacity: .6;
	  margin-bottom: 10px;
	  display: block;
	}
	
	.empty-state p {
	  margin-bottom: 16px;
	  font-size: .95rem;
	}
	
	.primary-btn {
	  padding: 10px 20px;
	  border-radius: 999px;
	  background: linear-gradient(135deg, #22c55e, #16a34a);
	  color: white;
	  border: none;
	  cursor: pointer;
	  font-size: .85rem;
	}
	
	.primary-btn:hover {
	  filter: brightness(1.1);
	}
	
	.reviews-filter-bar {
	  display: flex;
	  gap: 10px;
	  flex-wrap: wrap;
	  margin-bottom: 24px;
	}
	
	.filter-pill {
	  display: flex;
	  align-items: center;
	  gap: 8px;
	  padding: 8px 16px;
	  border-radius: 999px;
	  background: rgba(255,255,255,.04);
	  border: 1px solid rgba(255,255,255,.1);
	  color: #cfd2ff;
	  font-size: .85rem;
	  cursor: pointer;
	  transition: all .2s ease;
	}
	
	.filter-pill.active {
	  background: linear-gradient(135deg, #6366f1, #4f46e5);
	  border-color: transparent;
	  color: white;
	}
	
	.filter-pill.positive { color: #86efac; }
	.filter-pill.neutral  { color: #fde68a; }
	.filter-pill.negative { color: #fca5a5; }
	
	.filter-pill:hover {
	  background: rgba(255,255,255,.1);
	}
	
	.reviews-content {
	  background: rgba(20,22,40,.6);
	  border-radius: 20px;
	  padding: 32px;
	}
	
	.stub {
	  opacity: .6;
	}
	</style>