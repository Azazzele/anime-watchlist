import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/components/Home.vue'
import AnimeDetails from '@/components/AnimeDetails.vue'
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
    }
  ]
})

export default router
