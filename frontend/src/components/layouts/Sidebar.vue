<template>
  <aside
    class="bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 fixed top-0 left-0 h-screen pt-16 z-30 transition-all duration-300"
    :class="{
      'w-64': uiStore.isSidebarOpen, 
      'w-20': !uiStore.isSidebarOpen,
      'transform -translate-x-full': !isSidebarOpen && isMobile,
    }"
  >
    <div class="p-4">
      <h2 
        class="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4"
        :class="{ 'text-center': !uiStore.isSidebarOpen }"
      >
        {{ uiStore.isSidebarOpen ? 'MENU UTAMA' : 'M' }}
      </h2>
      <nav class="flex flex-col gap-2">
        <router-link to="/" class="flex items-center gap-3 px-4 py-2 rounded-md text-gray-700 dark:text-gray-200 font-medium hover:bg-blue-50 dark:hover:bg-gray-700 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" :class="{ 'justify-center': !uiStore.isSidebarOpen }">
          <span>📊</span>
          <span v-if="uiStore.isSidebarOpen">Dashboard</span>
        </router-link>
        
        <router-link to="/kalender" class="flex items-center gap-3 px-4 py-2 rounded-md text-gray-700 dark:text-gray-200 font-medium hover:bg-blue-50 dark:hover:bg-gray-700 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" :class="{ 'justify-center': !uiStore.isSidebarOpen }">
          <span>📅</span>
          <span v-if="uiStore.isSidebarOpen">Kalender Tim</span>
        </router-link>

        <router-link to="/dokumen" class="flex items-center gap-3 px-4 py-2 rounded-md text-gray-700 dark:text-gray-200 font-medium hover:bg-blue-50 dark:hover:bg-gray-700 hover:text-blue-600 dark:hover:text-blue-400 transition-colors" :class="{ 'justify-center': !uiStore.isSidebarOpen }">
          <span>📂</span>
          <span v-if="uiStore.isSidebarOpen">Pencarian Dokumen</span>
        </router-link>
      </nav>
    </div>
  </aside>
</template>

<script setup>
import { useUIStore } from '@/stores/ui';
import { onMounted, onUnmounted, ref } from 'vue';

const uiStore = useUIStore();

// Logika untuk mendeteksi layar mobile
const isMobile = ref(window.innerWidth < 768);
const updateIsMobile = () => {
  isMobile.value = window.innerWidth < 768;
  // Jika di desktop, pastikan sidebar selalu terlihat
  if (!isMobile.value && !uiStore.isSidebarOpen) {
      uiStore.isSidebarOpen = true;
  }
};
onMounted(() => window.addEventListener('resize', updateIsMobile));
onUnmounted(() => window.removeEventListener('resize', updateIsMobile));
</script>