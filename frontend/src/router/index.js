import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '@/views/LandingView.vue'
import DashboardView from '../views/DashboardView.vue'
import LoginView from '../views/LoginView.vue'
import AktivitasDashboardView from '../views/AktivitasDashboardView.vue'
import AktivitasDaftarView from '../views/AktivitasDaftarView.vue'
import AboutView from '@/views/AboutView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: AboutView
    },
    {
      path: '/aktivitas/dashboard',
      name: 'aktivitas-dashboard',
      component: AktivitasDashboardView
    },
    {
      path: '/aktivitas/daftar',
      name: 'aktivitas-daftar',
      component: AktivitasDaftarView
    },
    {
      path: '/aktivitas/detail/:id',
      name: 'aktivitas-detail',
      component: () => import('../views/AktivitasDetailView.vue')
    },
  ],
})

export default router
