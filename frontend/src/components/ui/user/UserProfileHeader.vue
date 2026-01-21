<script setup lang="ts">
	import { computed } from 'vue'
	import type { UserProfile } from '../../../types/user'
	
	const props = defineProps<{
		user: UserProfile
	}>()

	const bannerStyle = computed(() => ({
	backgroundImage: props.user.bannerImage
		? `url(${props.user.bannerImage})`
		: 'linear-gradient(135deg, #6366f1, #8b5cf6)'
	}))

	</script>
	
<template>
	<div class="profile-header">
	  <div class="banner" :style="bannerStyle"></div>
  
	  <div class="avatar-and-info">
		<div class="avatar-wrapper">
		  <img
			:src="user.avatar?.large || user.avatar?.medium || '/default-avatar.png'"
			:alt="user.name"
			class="avatar"
		  />
		</div>
  
		<div class="info">
		  <h1 class="username">{{ user.name }}</h1>
  
		  <div class="badges">
			<span v-if="user.moderatorRoles?.includes('ADMIN')" class="badge admin">
			  Admin
			</span>
			<span v-if="user.donatorTier" class="badge donator">
			  Donator Tier {{ user.donatorTier }}
			</span>
		  </div>
		</div>
	  </div>
	</div>
  </template>
  
 
  <style scoped>
  .profile-header {
	position: relative;
  }
  
  .banner {
	height: 220px;
	background-size: cover;
	background-position: center;
	background-repeat: no-repeat;
  }
  
  .avatar-and-info {
	position: relative;
	padding: 0 1rem 2rem;
	text-align: center;
  }
  
  .avatar-wrapper {
	width: 140px;
	height: 140px;
	margin: -70px auto 1rem;
	border-radius: 50%;
	overflow: hidden;
	border: 5px solid white;
	box-shadow: 0 10px 25px rgba(0,0,0,0.25);
	background: #e5e7eb;
  }
  
  .avatar {
	width: 100%;
	height: 100%;
	object-fit: cover;
  }
  
  .username {
	font-size: 2.5rem;
	font-weight: 700;
	margin-bottom: 0.5rem;
  }
  
  .badges {
	margin-top: 0.5rem;
  }
  
  .badge {
	padding: 0.4rem 1rem;
	border-radius: 20px;
	font-size: 0.9rem;
	font-weight: 600;
	margin: 0 0.4rem;
  }
  
  .badge.admin {
	background: #ef4444;
	color: white;
  }
  
  .badge.donator {
	background: #eab308;
	color: black;
  }
  
  @media (max-width: 640px) {
	.avatar-wrapper { width: 120px; height: 120px; margin: -60px auto 1rem; }
	.username { font-size: 2rem; }
  }
  </style>