<script setup>

</script>
<template>
	<nav class='conteiner'>
		<div>
			<h2>Jukey</h2>	
		</div>
		<div class='wrapper_conteiner'>
			<ul class='list'>
				<li><a href="/">Главная</a></li>
				<li><a href="">Аниме</a></li>
				<li><a href="">Манга</a></li>
				<li><a href="">Ранобэ</a></li>
				<li><a href="">Новеллы</a></li>
				<li><a href="">Форум</a></li>
			</ul>
		</div>
		<div class="search">
			<span class="material-symbols-outlined search-icon">
				search
			</span>
			<input type="text" placeholder="Поиск..." />
		</div>
		<div class="auth">
			<button>Вход</button>
			<button>Регистрация</button>
		</div>
	</nav>
</template>
<style>
@import url("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined");
@import '../assets/main.css';

	/* ===== SEARCH ===== */
.search {
	display: flex;
	left: 0;
	width: 640px;
	align-items: center;
	justify-content: left;
	gap: 8px;
	padding: 6px 12px;
	border-radius: 12px;
	border: 1.5px solid var(--text-main)
}

.search-icon {
	color: var(--text-main);
	font-size: 14px;
}

.search input {
	background: transparent;
	border: none;
	outline: none;
	color: var(--text-main);
	font-size: 14px;
	width: 160px;
	font-family: inherit;
	
}

.search input::placeholder {
	color: var(--text-main);
}

/* ===== AUTH BUTTON ===== */
.auth{
	display: flex;
	align-items: center;
}
.auth button {
	background: transparent;
	border: none;
	padding: 8px 18px;
	border-radius: 10px;
	margin-left: 10px;
	font-weight: 600;
	cursor: pointer;
	transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.auth button:hover {
	color: var(--accent-primary);
	transition: var(--transition-base)
}
/* ===== ICONS ===== */
.material-symbols-outlined {
	font-variation-settings:
		'FILL' 0,
		'wght' 400,
		'GRAD' 0,
		'opsz' 24;
	font-size: 20px;
	line-height: 1;
}

/* SEARCH ICON */
.search-icon {
	color: var(--text-main);
	font-size: 18px;
}

</style>