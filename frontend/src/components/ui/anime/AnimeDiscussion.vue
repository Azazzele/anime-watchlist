<script setup lang="ts">
	import { ref, computed } from 'vue'
	
	/* ================= USER ================= */
	const currentUser = 'Kira_Yagami'
	
	/* ================= REVIEWS ================= */
	type ReviewType = 'all' | 'positive' | 'neutral' | 'negative'
	
	interface Review {
	  id: number
	  type: Exclude<ReviewType, 'all'>
	  text: string
	}
	
	const reviews = ref<Review[]>([])
	const activeReviewFilter = ref<ReviewType>('all')
	
	const reviewCounters = computed(() => ({
	  all: reviews.value.length,
	  positive: reviews.value.filter(r => r.type === 'positive').length,
	  neutral: reviews.value.filter(r => r.type === 'neutral').length,
	  negative: reviews.value.filter(r => r.type === 'negative').length,
	}))
	
	const filteredReviews = computed(() => {
	  if (activeReviewFilter.value === 'all') return reviews.value
	  return reviews.value.filter(r => r.type === activeReviewFilter.value)
	})
	
	/* ================= COMMENTS ================= */
	interface Comment {
	  id: number
	  author: string
	  avatar: string
	  text: string
	  createdAt: string
	}
	
	const comments = ref<Comment[]>([
	  {
		id: 1,
		author: 'Kira_Yagami',
		avatar: 'https://i.pravatar.cc/80?img=12',
		text: `Очень достойный тайтл.
	Сюжет затягивает, музыка шикарная.`,
		createdAt: '2 часа назад'
	  },
	  {
		id: 2,
		author: 'Ryuk',
		avatar: 'https://i.pravatar.cc/80?img=32',
		text: `@Kira_Yagami полностью согласен, особенно опенинг 🔥`,
		createdAt: '1 час назад'
	  }
	])
	
	/* ================= ADD COMMENT ================= */
	const newComment = ref('')
	
	const sendComment = () => {
	  if (!newComment.value.trim()) return
	
	  comments.value.push({
		id: Date.now(),
		author: currentUser,
		avatar: 'https://i.pravatar.cc/80?img=68',
		text: newComment.value,
		createdAt: 'только что'
	  })
	
	  newComment.value = ''
	}
	
	/* ================= EDIT ================= */
	const editingId = ref<number | null>(null)
	const editText = ref('')
	
	const startEdit = (c: Comment) => {
	  editingId.value = c.id
	  editText.value = c.text
	}
	
	const cancelEdit = () => {
	  editingId.value = null
	  editText.value = ''
	}
	
	const saveEdit = (id: number) => {
	  const c = comments.value.find(c => c.id === id)
	  if (!c) return
	  c.text = editText.value
	  cancelEdit()
	}
	
	const deleteComment = (id: number) => {
	  comments.value = comments.value.filter(c => c.id !== id)
	}
	
	/* ================= MENTION TOOLTIP ================= */
	const hoveredUser = ref<Comment | null>(null)
	const tooltipPos = ref({ x: 0, y: 0 })
	
	const showMention = (username: string, e: MouseEvent) => {
	  const found = comments.value.find(c => c.author === username)
	  if (!found) return
	  hoveredUser.value = found
	  tooltipPos.value = { x: e.clientX + 12, y: e.clientY + 12 }
	}
	
	const hideMention = () => hoveredUser.value = null
	
	/* ================= TABS ================= */
	const activeDiscussionTab = ref<'comments' | 'reviews'>('comments')
	</script>
	
	<template>
	<section class="discussion">
	
	<header class="discussion-header">
	  <nav class="tabs">
		<button :class="{active:activeDiscussionTab==='comments'}" @click="activeDiscussionTab='comments'">
		  Комментарии
		</button>
		<button :class="{active:activeDiscussionTab==='reviews'}" @click="activeDiscussionTab='reviews'">
		  Отзывы
		</button>
	  </nav>
	</header>
	
	<!-- ================= COMMENTS ================= -->
	<div v-if="activeDiscussionTab==='comments'">
	
	  <div v-for="comment in comments" :key="comment.id" class="comment">
	
		<img class="avatar" :src="comment.avatar" />
	
		<div class="comment-body">
	
		  <div class="comment-meta">
			<span class="author">{{ comment.author }}</span>
			<span class="date">{{ comment.createdAt }}</span>
		  </div>
	
		  <!-- EDIT -->
		  <template v-if="editingId===comment.id">
			<textarea v-model="editText" class="edit-textarea" />
			<div class="edit-actions">
			  <button class="btn" @click="saveEdit(comment.id)">Сохранить</button>
			  <button class="btn cancel" @click="cancelEdit">Отмена</button>
			</div>
		  </template>
	
		  <!-- TEXT -->
		  <template v-else>
			<p class="comment-text">
			  <template v-for="(part,i) in comment.text.split(/(@[^\s@]+)/g)" :key="i">
				<span
				  v-if="part.startsWith('@')"
				  class="mention"
				  @mouseenter="showMention(part.slice(1),$event)"
				  @mouseleave="hideMention"
				>
				  {{ part }}
				</span>
				<span v-else>{{ part }}</span>
			  </template>
			</p>
		  </template>
		</div>
	
		<!-- ACTIONS -->
		<div class="comment-actions">
		  <button class="action-btn" title="Ответить">
			<span class="material-symbols-outlined">reply</span>
		  </button>
	
		  <button
			v-if="comment.author!==currentUser"
			class="action-btn danger"
			title="Пожаловаться"
		  >
			<span class="material-symbols-outlined">flag</span>
		  </button>
	
		  <button
			v-if="comment.author===currentUser"
			class="action-btn"
			title="Редактировать"
			@click="startEdit(comment)"
		  >
			<span class="material-symbols-outlined">edit</span>
		  </button>
	
		  <button
			v-if="comment.author===currentUser"
			class="action-btn danger"
			title="Удалить"
			@click="deleteComment(comment.id)"
		  >
			<span class="material-symbols-outlined">delete</span>
		  </button>
		</div>
	  </div>
	
	  <!-- FORM -->
	  <div class="comment-form">
		<img class="avatar" src="https://i.pravatar.cc/80?img=68" />
		<div class="form-body">
		  <textarea
			v-model="newComment"
			placeholder="Написать комментарий…"
		  />
		  <div class="form-actions">
			<button class="send" :disabled="!newComment.trim()" @click="sendComment">
			  Отправить
			</button>
		  </div>
		</div>
	  </div>
	</div>
	
	<!-- ================= REVIEWS ================= -->
	<div v-else class="block">
	  <div class="reviews-filter-bar">
		<button class="filter all" :class="{active:activeReviewFilter==='all'}">Все ({{reviewCounters.all}})</button>
		<button class="filter positive" :class="{active:activeReviewFilter==='positive'}">Положительные</button>
		<button class="filter neutral" :class="{active:activeReviewFilter==='neutral'}">Нейтральные</button>
		<button class="filter negative" :class="{active:activeReviewFilter==='negative'}">Отрицательные</button>
	  </div>
	</div>
	
	</section>
	
	<!-- TOOLTIP -->
	<div
	  v-if="hoveredUser"
	  class="mention-tooltip"
	  :style="{top:tooltipPos.y+'px',left:tooltipPos.x+'px'}"
	>
	  <img :src="hoveredUser.avatar" />
	  <div>
		<b>{{ hoveredUser.author }}</b>
		<div class="tooltip-text">{{ hoveredUser.text }}</div>
	  </div>
	</div>
	</template>dp
	
	<style scoped>
	/* ===== BASIC ===== */
	
	.discussion {
	  margin: 64px auto;
	  padding: 0 24px;
	  color: #e5e7eb;
	}
	
	.tabs {
	  display: flex;
	  gap: 24px;
	  margin-bottom: 1.5em;
	}
	
	.tabs button {
	  background: none;
	  border: none;
	  font-size: 18px;
	  color: #777;
	  cursor: pointer;
	}
	
	.tabs button.active {
	  color: #fff;
	  font-weight: 600;
	}
	
	/* ===== COMMENTS ===== */
	
	.comment {
	  display: flex;
	  gap: 14px;
	  padding: 16px 0;
	  border-bottom: 1px solid #2a2a2a;
	}
	
	.avatar {
	  width: 48px;
	  height: 48px;
	  border-radius: 50%;
	}
	
	.comment-body {
	  flex: 1;
	}
	
	.comment-meta {
	  font-size: 14px;
	  color: #888;
	}
	
	.author {
	  color: #fff;
	  font-weight: 600;
	}
	
	.date {
	  margin-left: 6px;
	}
	
	.comment-text {
	  line-height: 1.6;
	}
	
	/* ===== MENTION ===== */
	
	.mention {
	  color: #60a5fa;
	  cursor: pointer;
	}
	
	.mention:hover {
	  text-decoration: underline;
	}
	
	/* ===== TOOLTIP ===== */
	
	.mention-tooltip {
	  position: fixed;
	  z-index: 999;
	  background: #111;
	  border: 1px solid #2a2a2a;
	  border-radius: 10px;
	  padding: 12px;
	  display: flex;
	  gap: 10px;
	  max-width: 360px;
	  box-shadow: 0 10px 30px rgba(0,0,0,.6);
	}
	
	.tooltip-text {
	  max-height: 80px;
	  overflow: hidden;
	  color: #cbd5f5;
	}
	
	/* ===== FORM ===== */
	
	.comment-form {
  display: flex;
  gap: 14px;
  padding: 16px;
  margin-top: 24px;
  background: none;
  border-radius: 12px;
}

.comment-form .avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
}

.form-body {
  flex: 1;
}

.comment-form textarea {
  width: 100%;
  min-height: 140px;
  resize: vertical;
  padding: 14px 16px;
  background: #0b0b0b;
  border: 1px solid #2a2a2a;
  border-radius: 10px;
  color: #e5e7eb;
  font-size: 15px;
  line-height: 1.6;
  font-family: inherit;
  font-size: 18px;
}

.comment-form textarea::placeholder {
  color: #6b7280;
  font-size: 18px;
}

.comment-form textarea:focus {
  outline: none;
  box-shadow: 0 0 0 2px rgba(96,165,250,.2);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.send {
  background: #22c55e;
  border: none;
  color: #000;
  padding: 8px 18px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.send:disabled {
  opacity: .4;
  cursor: default;
}

	
	/* ===== ACTIONS ===== */
	
	.comment {
  display: flex;
  gap: 14px;
  padding: 16px 0;
  border-bottom: 1px solid #2a2a2a;
  align-items: flex-start;
}

.comment-actions {
  margin-left: auto;              /* ← ВАЖНО */
  display: flex;
  gap: 6px;
  opacity: 0;
  transition: opacity .15s ease;
}

.comment:hover .comment-actions {
  opacity: 1;
}

.action-btn {
  background: none;
  border: none;
  padding: 6px;
  border-radius: 6px;
  cursor: pointer;
  color: #9ca3af;
}

.action-btn:hover {
  background: #2a2a2a;
  color: #fff;
}

.action-btn.danger:hover {
  color: #ef4444;
}

.material-symbols-outlined {
  font-size: 20px;
}

	/* ===== FILTERS ===== */

.reviews-filter-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
}

.filter {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 18px;
  border-radius: 12px;
  background: #1a1a1a;
  border: none;
  cursor: pointer;
  transition: .25s;
  color: #aaa;
  white-space: nowrap;
}

.filter > span {
  font-weight: 700;
  font-size: 18px;
}

.filter.active {
  flex: 1;
  color: #fff;
  background-color: #2c2b2b;
}

/* ЦВЕТА */
.filter.positive.active {
  background: #22c55e;
}

.filter.neutral.active {
  background: #facc15;
  color: #000;
}

.filter.negative.active {
  background: #ef4444;
}

/* иконки */
.material-symbols-outlined {
  font-size: 20px;
}
.edit-textarea {
  width: 100%;
  min-height: 120px;
  background: #111;
  border: 1px solid #2a2a2a;
  border-radius: 8px;
  padding: 12px;
  color: #fff;
  font-size: 15px;
  resize: vertical;
}

.edit-actions {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.btn.cancel {
  background: #2a2a2a;
  color: #aaa;
}

	</style>
	