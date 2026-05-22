import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue')
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/letters',
    name: 'Letters',
    component: () => import('@/views/Letters.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/letters/:id',
    name: 'LetterDetail',
    component: () => import('@/views/LetterDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/write',
    name: 'WriteLetter',
    component: () => import('@/views/WriteLetter.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/checklist/:id',
    name: 'Checklist',
    component: () => import('@/views/Checklist.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/vaccine/:id',
    name: 'VaccineRecords',
    component: () => import('@/views/VaccineRecords.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/health/:id',
    name: 'HealthRecords',
    component: () => import('@/views/HealthRecords.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router
