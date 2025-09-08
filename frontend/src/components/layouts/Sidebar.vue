<template>
  <aside
    class="bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 fixed top-0 left-0 h-screen pt-16 z-30 transition-all duration-300 overflow-y-auto"
    :class="{
      'w-64': uiStore.isSidebarOpen, 
      'w-20': !uiStore.isSidebarOpen,
      'transform -translate-x-full': !uiStore.isSidebarOpen && isMobile,
    }"
  >
    <div class="p-4">
      <nav class="flex flex-col gap-1">
        <div v-for="item in menuItems" :key="item.label">
          <router-link v-if="!item.children" :to="item.to" class="flex items-center gap-3 px-4 py-2.5 rounded-md text-gray-600 dark:text-gray-300 font-medium hover:bg-blue-50 dark:hover:bg-gray-700 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" :class="{ 'justify-center': !uiStore.isSidebarOpen }">
            <span v-html="item.icon" class="text-xl"></span>
            <span v-if="uiStore.isSidebarOpen">{{ item.label }}</span>
          </router-link>
          
          <div v-else>
            <button @click="toggleDropdown(item.label)" class="w-full flex items-center justify-between gap-3 px-4 py-2.5 rounded-md text-gray-600 dark:text-gray-300 font-medium hover:bg-blue-50 dark:hover:bg-gray-700 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" :class="{ 'justify-center': !uiStore.isSidebarOpen }">
              <div class="flex items-center gap-3">
                <span v-html="item.icon" class="text-xl"></span>
                <span v-if="uiStore.isSidebarOpen">{{ item.label }}</span>
              </div>
              <svg v-if="uiStore.isSidebarOpen" class="h-4 w-4 transition-transform duration-200" :class="{ 'rotate-90': openDropdowns[item.label] }" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" /></svg>
            </button>
            
            <transition name="expand">
              <div v-if="openDropdowns[item.label] && uiStore.isSidebarOpen" class="mt-1 ml-7 pl-3 border-l border-gray-200 dark:border-gray-600 overflow-hidden">
                <router-link v-for="child in item.children" :key="child.label" :to="child.to" class="flex items-center gap-3 px-4 py-2 rounded-md text-sm text-gray-500 dark:text-gray-400 font-medium hover:bg-blue-50 dark:hover:bg-gray-700 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                  {{ child.label }}
                </router-link>
              </div>
            </transition>
          </div>
        </div>
      </nav>
    </div>
  </aside>
</template>

<script setup>
import { useUIStore } from '@/stores/ui';
import { onMounted, onUnmounted, ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';

const uiStore = useUIStore();
const authStore = useAuthStore();

// Logika untuk mendeteksi layar mobile
const isMobile = ref(window.innerWidth < 768);
const updateIsMobile = () => { isMobile.value = window.innerWidth < 768; };
onMounted(() => window.addEventListener('resize', updateIsMobile));
onUnmounted(() => window.removeEventListener('resize', updateIsMobile));

// Struktur Menu (tidak berubah)
const menuItems = computed(() => {
  const baseMenu = [
    { label: 'Dashboard', to: '/dashboard', icon: '📊' },
    { label: 'Kalender', to: '/kalender', icon: '📅' },
    { label: 'Team', to: '/team', icon: '👥'},
    { label: 'Project', to: '/project', icon: '💼'},
    { 
      label: 'Aktivitas', to: '/aktivitas/daftar', icon: '✅'
    },
  ];
  if (authStore.isAdmin) {
    baseMenu.push({
      label: 'Admin', 
      icon: '⚙️',
      children: [
        { label: 'Manajemen User', to: '/admin/users' },
        { label: 'Manajemen Tim', to: '/admin/teams'},
      ]
    });
  }

  return baseMenu;
});



// 1. Gunakan ref({}) sebagai ganti reactive({}) untuk fleksibilitas.
const openDropdowns = ref({});

// 2. Ganti total fungsi toggleDropdown dengan logika baru.
const toggleDropdown = (label) => {
  // Cek apakah dropdown yang diklik saat ini sudah terbuka.
  const isCurrentlyOpen = openDropdowns.value[label];

  // Selalu tutup semua dropdown terlebih dahulu.
  openDropdowns.value = {};

  // Jika dropdown yang diklik tadi posisinya tertutup, maka sekarang buka.
  if (!isCurrentlyOpen) {
    openDropdowns.value[label] = true;
  }
  // Jika sudah terbuka, ia akan tetap tertutup karena sudah direset di atas.
};
</script>

<style scoped>
/* CSS untuk transisi expand/collapse yang halus */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease-in-out;
  max-height: 200px;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
  transform: translateY(-10px);
}
</style>  