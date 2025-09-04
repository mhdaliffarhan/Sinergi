import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

import LandingView from '@/views/LandingView.vue'
import DashboardView from '../views/DashboardView.vue'
import LoginView from '../views/LoginView.vue'
import AktivitasDashboardView from '../views/AktivitasDashboardView.vue'
import AktivitasDaftarView from '../views/AktivitasDaftarView.vue'
import AboutView from '@/views/AboutView.vue'
import ProfileView from '@/views/ProfileView.vue'
import ProjectView from '@/views/ProjectView.vue'

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
      path: '/profil',
      name: 'profil',
      component: ProfileView,
      meta: { requiresAuth: true }
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: AboutView,
      meta: { requiresAuth: true }
    },
    {
      path: '/project',
      name: 'project',
      component: ProjectView,
      meta: { requiredAuth: true }
    },
    {
      path: '/project/detail/:id',
      name: 'project-detail',
      component: () => import('../views/ProjectDetailView.vue'),
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
    {
      path: '/kalender-tim',
      name: 'kalender-tim',
      component: () => import('../views/KalenderTimView.vue'),
      meta: { requiredAuth: true }
    },
    {
      path: '/kalender-pegawai',
      name: 'kalender-pegawai',
      component: () => import('../views/KalenderPegawaiView.vue'),
      meta: { requiredAuth: true }
    },
    {
      path: '/admin/users',
      name: 'manajemen-user',
      component: () => import('../views/admin/UserManagementView.vue'),
      meta: {
        requiresAuth: true,
        requiredRoles: ['Superadmin', 'Admin']
      }
    },
    {
      path: '/admin/teams',
      name: 'admin-teams',
      component: () => import('../views/admin/TeamManagementView.vue'),
      meta: {
        requiresAuth: true,
        requiredRoles: ['Superadmin', 'Admin']
      }
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();
  const toast = useToast();

  if (authStore.token && !authStore.user) {
    await authStore.fetchUser();
  }

  const isAuthenticated = authStore.isAuthenticated;
  const userRole = authStore.user?.sistemRole?.namaRole;

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: 'login' });
  }

  if (to.meta.requiredRoles && isAuthenticated) {
    if (!to.meta.requiredRoles.includes(userRole)) {
      toast.error("Anda tidak memiliki hak akses ke halaman ini.");
      return next({ name: 'dashboard' });
    }
  }

  next();
});

export default router
