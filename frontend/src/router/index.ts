import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Home from '../components/page/Home.vue'
import AnimeDetails from '../components/page/AnimeDetails.vue'
import CharacterDetail from '../components/page/CharacterDetail.vue'
// import AnimeCharactersList from '../components/page/AnimeCharactersList.vue' 

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: Home,
    meta: { title: 'Главная' }
  },
  {
    path: '/anime/:id(\\d+)',
    name: 'anime-details',
    component: AnimeDetails,
    props: route => ({
      id: Number(route.params.id),
      type: 'anime'
    })
  },
  {
    path: '/manga/:id(\\d+)',
    name: 'manga-details',
    component: AnimeDetails,
    props: route => ({
      id: Number(route.params.id),
      type: 'manga'
    })
  },
  {
    path: '/ranobe/:id(\\d+)',
    name: 'ranobe-details',
    component: AnimeDetails,
    props: route => ({
      id: Number(route.params.id),
      type: 'ranobe'
    })
  },  
  {
    path: '/media/:type(anime|manga|ranobe)/:id(\\d+)',
    name: 'media-details',
    component: AnimeDetails, // ДА, тот же компонент
    props: route => ({
      id: Number(route.params.id),
      type: route.params.type
    }),
    meta: { title: 'Детали медиа' }
  },
  {
    path: '/character/:characterId(\\d+)',
    name: 'character',
    component: CharacterDetail,
    props: route => ({
      characterId: Number(route.params.characterId),
    }),
    meta: { title: 'Персонаж' }
  },
  {
    path: '/staff/:staffId(\\d+)',
    name: 'staff',
    component: () => import('../components/page/Staf.vue'),
    props: true,
    meta: { title: 'Персонаж персонала' }
  },
  {
    path: '/media/:type(anime|manga|ranobe)/:id(\\d+)/characters',
    name: 'media-characters',
    component: () => import('../components/page/AnimeCharactersList.vue'),
    props: route => ({
      id: Number(route.params.id),
      type: route.params.type
    }),
    meta: { title: 'Персонажи' }
  },  

  // 404 — catch-all (опционально)
//  {
 //   path: '/:pathMatch(.*)*',
//    name: 'not-found',
//    component: () => import('../components/page/NotFound.vue'),
 //   meta: { title: 'Страница не найдена' }
 // }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach((to, from, next) => {
  document.title = (to.meta.title as string) || 'WordAnimation'
  next()
})
export default router