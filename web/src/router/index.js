// Composables
import {createRouter, createWebHistory} from 'vue-router'


const routes = [
  {
    path: '/chat',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        component: () => import('@/views/Chat.vue'),
      },
      {
        path: ':id',
        component: () => import('@/views/Chat.vue'),
      },
    ],
  },
  {
    path: '/login',
    component: () => import('@/layouts/login/Login.vue'),
    children: [
      {
        path: '',
        component: () => import('@/views/Login.vue'),
      }
    ]
  },
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        component: () => import('@/views/Home.vue'),
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
