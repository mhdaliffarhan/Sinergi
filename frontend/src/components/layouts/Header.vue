<template>
  <header class="bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm border-b border-gray-200 dark:border-gray-700 fixed top-0 left-0 right-0 z-40">
    <div class="px-4 sm:px-6 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <button @click="uiStore.toggleSidebar" class="p-2 rounded-full text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" /></svg>
        </button>
        <router-link to="/dashboard" class="flex items-center">
          <img src="/logo-tulisan.png" alt="Logo SINERGI" class="pt-2 w-32 h-full object-contain">
        </router-link>
      </div>
      <div class="flex items-center gap-2">
        
      </div>
  
      <div class="flex items-center gap-2 sm:gap-4">

        <Menu as="div" class="relative">
          <MenuButton class="p-2 rounded-full  text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
            <svg v-if="theme === 'light'" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" /></svg>
            <svg v-if="theme === 'dark'" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" /></svg>
            <svg v-if="theme === 'system'" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
          </MenuButton>
          <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
            <MenuItems class="absolute right-0 mt-2 w-32 origin-top-right border border-gray-200 dark:border-gray-700 divide-y divide-gray-100 dark:divide-gray-600 rounded-md bg-white dark:bg-gray-800 shadow-lg  focus:outline-none">
              <div class="px-1 py-1">
                <MenuItem v-slot="{ active }">
                  <button @click="setTheme('light')" :class="[active ? 'bg-blue-500 text-white' : 'text-gray-900 dark:text-gray-200', 'group flex w-full items-center rounded-md px-2 py-2 text-sm']">Light</button>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                  <button @click="setTheme('dark')" :class="[active ? 'bg-blue-500 text-white' : 'text-gray-900 dark:text-gray-200', 'group flex w-full items-center rounded-md px-2 py-2 text-sm']">Dark</button>
                </MenuItem>
                <MenuItem v-slot="{ active }">
                  <button @click="setTheme('system')" :class="[active ? 'bg-blue-500 text-white' : 'text-gray-900 dark:text-gray-200', 'group flex w-full items-center rounded-md px-2 py-2 text-sm']">System</button>
                </MenuItem>
              </div>
            </MenuItems>
          </transition>
        </Menu>

        <button class="p-2 rounded-full text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700">
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6 6 0 00-4-5.659V5a2 2 0 10-4 0v.341A6 6 0 006 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" /></svg>
        </button>

        <Menu as="div" class="relative">
          <MenuButton class="flex items-center">
            <img class="h-9 w-9 rounded-full object-cover" src="/profile-default.png" alt="User profile photo" />
          </MenuButton>
          <transition enter-active-class="transition ease-out duration-100" enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100" leave-active-class="transition ease-in duration-75" leave-from-class="transform opacity-100 scale-100" leave-to-class="transform opacity-0 scale-95">
            <MenuItems class="absolute right-0 mt-2 w-48 origin-top-right divide-y divide-gray-100 dark:divide-gray-600 rounded-md bg-white dark:bg-gray-800 shadow-lg broder border-gray-200 dark:border-gray-700 focus:outline-none">
              <div class="px-1 py-1">
                <div class="px-2 py-2">
                  <p class="text-sm font-semibold text-gray-900 dark:text-white">{{ authStore.user?.namaLengkap || 'Memuat...' }}</p>
                  <p class="text-sm text-gray-500 dark:text-gray-400 truncate">{{ authStore.user?.username }}</p>
                </div>
              </div>
              <div class="px-1 py-1">
                <MenuItem v-slot="{ active }">
                  <button :class="[active ? 'bg-blue-500 text-white' : 'text-gray-900 dark:text-gray-200', 'group flex w-full items-center rounded-md px-2 py-2 text-sm']">Profil</button>
                </MenuItem>
              </div>
              <div class="px-1 py-1">
                <MenuItem v-slot="{ active }">
                  <button @click="authStore.logout" :class="[active ? 'bg-blue-500 text-white' : 'text-gray-900 dark:text-gray-200', 'group flex w-full items-center rounded-md px-2 py-2 text-sm']">
                    Logout
                  </button>
                </MenuItem>
              </div>
            </MenuItems>
          </transition>
        </Menu>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useUIStore } from '@/stores/ui';
import { useAuthStore } from '@/stores/auth';
import { ref, onMounted} from 'vue';
import { Menu, MenuButton, MenuItems, MenuItem } from '@headlessui/vue'

const uiStore = useUIStore();
const authStore = useAuthStore();

// 1. STATE: Gunakan satu ref untuk menyimpan tema saat ini.
// Ambil dari localStorage, atau default ke 'system'.
const theme = ref(localStorage.getItem('theme') || 'system');

// 2. HELPER FUNCTION: Logika utama untuk menerapkan tema.
const applyTheme = (newTheme) => {
  if (newTheme === 'dark') {
    // Jika tema adalah 'dark', selalu tambahkan kelas 'dark'.
    document.documentElement.classList.add('dark');
  } else if (newTheme === 'light') {
    // Jika tema adalah 'light', selalu hapus kelas 'dark'.
    document.documentElement.classList.remove('dark');
  } else {
    // Jika tema adalah 'system', periksa preferensi OS.
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }
};

// 3. ACTION: Fungsi yang dipanggil saat tombol diklik.
const setTheme = (newTheme) => {
  theme.value = newTheme;
  localStorage.setItem('theme', newTheme);
  applyTheme(newTheme);
};

// 4. LIFECYCLE HOOK: Terapkan tema saat aplikasi dimuat dan dengarkan perubahan OS.
const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
const handleSystemThemeChange = () => {
  // Hanya terapkan perubahan jika tema saat ini adalah 'system'.
  if (theme.value === 'system') {
    applyTheme('system');
  }
};

onMounted(() => {
  applyTheme(theme.value);
  // Dengarkan perubahan tema sistem
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    if (theme.value === 'system') {
      applyTheme('system');
    }
  });
});
</script>