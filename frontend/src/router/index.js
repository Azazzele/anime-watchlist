import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import AnimeDetails from '@/components/AnimeDetails.vue'
import CharacterDetail from '@/components/page/CharacterDetail.vue'

import 'material-symbols'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/anime/:id',
      name: 'anime-details',
      component: AnimeDetails
    },
    {
      path: '/anime/:animeId/character/:characterId',
      name: 'character',
      component: CharacterDetail,
      props: true,
    },
    {
      path: '/anime/:animeId/characters',
      name: 'anime-characters',
      props: true,
    }
  ]
})

export default router
