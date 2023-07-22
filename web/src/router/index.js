// Composables
import {createRouter, createWebHistory} from 'vue-router'


const routes = [
  {
    path: '/chat',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: '聊天',
        component: () => import(/* webpackChunkName: "home" */ '@/views/Chat.vue'),
      },
    ],
  },
  {
    path: '/login',
    component: () => import('@/layouts/login/Login.vue'),
    children: [
      {
        path: '',
        name: '登录',
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
        name: '首页 (跳转)',
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
