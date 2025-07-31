import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

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
      component: AboutView,
      meta: { requiresAuth: true }
    },
    {
      path: '/aktivitas/dashboard',
      name: 'aktivitas-dashboard',
      component: AktivitasDashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/aktivitas/daftar',
      name: 'aktivitas-daftar',
      component: AktivitasDaftarView,
      meta: { requiresAuth: true }
    },
    {
      path: '/aktivitas/detail/:id',
      name: 'aktivitas-detail',
      component: () => import('../views/AktivitasDetailView.vue'),
      meta: { requiresAuth: true }
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Jika ada token tapi belum ada data user, coba ambil dulu
  if (authStore.token && !authStore.user) {
    await authStore.fetchUser();
  }

  // Jika halaman tujuan butuh login DAN pengguna belum login
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Arahkan (redirect) pengguna ke halaman login
    next({ name: 'login' })
  } else {
    // Jika tidak, biarkan pengguna melanjutkan
    next()
  }
})

export default router
