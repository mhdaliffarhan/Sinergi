<template>
  <header class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 fixed top-0 left-0 right-0 z-40">
    <div class="px-4 h-16 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <button @click="uiStore.toggleSidebar" class="p-2 rounded-full text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
        <img src="/logo-tulisan-panjang.png" alt="Logo Tulisan" class="mt-2 h-64">
      </div>
  
      <div class="flex items-center gap-4">
        <button @click="toggleDarkMode" class="p-2 rounded-full text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
          <svg v-if="isDark" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>
          <svg v-else class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
        </button>
        <div class="flex items-center">
          <img class="h-9 w-9 rounded-full object-cover" src="https://via.placeholder.com/150" alt="User profile photo" />
          <div class="ml-2 text-sm hidden md:block">
            <p class="font-semibold text-gray-700 dark:text-gray-200">Nama Pengguna</p>
            <p class="text-gray-500 dark:text-gray-400">Jabatan</p>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useUIStore } from '@/stores/ui';
import { ref, onMounted } from 'vue';

const uiStore = useUIStore();

// Logika untuk Dark Mode
const isDark = ref(false);
const toggleDarkMode = () => {
  isDark.value = !isDark.value;
  if (isDark.value) {
    document.documentElement.classList.add('dark');
    localStorage.setItem('theme', 'dark');
  } else {
    document.documentElement.classList.remove('dark');
    localStorage.setItem('theme', 'light');
  }
};

// Cek tema saat komponen dimuat
onMounted(() => {
  if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true;
    document.documentElement.classList.add('dark');
  } else {
    isDark.value = false;
    document.documentElement.classList.remove('dark');
  }
});
</script>