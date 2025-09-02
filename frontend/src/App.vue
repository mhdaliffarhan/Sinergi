<template>
  <div v-if="showMainLayout" class="dark:bg-gray-900">  
    <div class="flex h-screen">
      <Sidebar />

      <div 
        class="flex-1 flex flex-col overflow-hidden transition-all duration-300"
        :class="{'md:ml-64': uiStore.isSidebarOpen, 'md:ml-20': !uiStore.isSidebarOpen}"
      >

        <Header />

        <main class="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50 dark:bg-gray-900 pt-16 p-6 pt-20 md:px-16">
          <router-view />
        </main>
      </div>
      <div
        v-if="uiStore.isSidebarOpen && isMobile"
        @click="uiStore.closeSidebar"
        class="fixed inset-0 bg-transparent z-20 md:hidden"
      ></div>
    </div>
  </div>
  <div v-else>
    <router-view />
  </div>
</template>

<script setup>
import Header from '@/components/layouts/Header.vue';
import Sidebar from '@/components/layouts/Sidebar.vue';
import { useUIStore } from '@/stores/ui';
import { computed, ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const uiStore = useUIStore();

// Buat sebuah computed property yang akan bernilai 'true' atau 'false'
// berdasarkan nama rute saat ini.
const showMainLayout = computed(() => {
  const layoutLessRoutes = ['login', 'landing'];

  return !layoutLessRoutes.includes(route.name);
});

// Logika untuk mendeteksi layar mobile, kita pindahkan ke App.vue
const isMobile = ref(window.innerWidth < 768);
const updateIsMobile = () => {
  isMobile.value = window.innerWidth < 768;
};
onMounted(() => window.addEventListener('resize', updateIsMobile));
onUnmounted(() => window.removeEventListener('resize', updateIsMobile));
</script>

<style>
</style>