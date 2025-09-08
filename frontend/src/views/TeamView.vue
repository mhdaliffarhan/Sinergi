<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-green-700 dark:text-green-500">Daftar Tim Aktif</h1>
        <div class="mt-4 relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
          </div>
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="Cari Tim..."
            class="block w-full sm:w-96 pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md leading-5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div> 
      </div>
      <div class="mt-4 sm:mt-0 flex items-center gap-2">
        <div class="relative inline-flex items-center bg-gray-100 dark:bg-gray-700 p-1 rounded-lg">
          <span
            class="absolute top-1 bottom-1 left-1 w-[calc(50%-0.25rem)] bg-orange-500 rounded-md shadow-md transition-transform duration-300 ease-in-out"
            :class="{ 'translate-x-full': viewMode === 'table' }"
          ></span>
          <button
            @click="viewMode = 'card'"
            class="relative z-10 w-1/2 px-3 py-1.5 flex justify-center items-center transition-colors duration-300"
            :class="viewMode === 'card' ? 'text-white' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
          </button>
          
          <button
            @click="viewMode = 'table'"
            class="relative z-10 w-1/2 px-3 py-1.5 flex justify-center items-center transition-colors duration-300"
            :class="viewMode === 'table' ? 'text-white' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path></svg>
          </button>
        </div>
      </div>
    </div>

    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <svg class="animate-spin -ml-1 mr-3 h-10 w-10 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>
    
    <div v-else class="mt-6">
      <div v-if="teams.length > 0" class="card-grid">
        <DaftarTeam v-if="viewMode === 'card'" :teams="teams" />
        <TabelTeam v-if="viewMode === 'table'" :teams="teams" />
      </div>
      <div v-else class="text-center text-gray-500 dark:text-gray-400">
        Tidak ada tim aktif yang ditemukan.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { useAuthStore } from '@/stores/auth';

import DaftarTeam from '@/components/team/DaftarTeam.vue';
import TabelTeam from '@/components/team/TabelTeam.vue';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormTim from '@/components/admin/FormTim.vue';

const baseURL = import.meta.env.VITE_API_BASE_URL;
const authStore = useAuthStore();
const toast = useToast();
const teams = ref([]);
const isModalOpen = ref(false);
const viewMode = ref('table');
const isLoading = ref(false);
const searchQuery = ref('');
let debounceTimer = null;

const updateViewMode = () => {
  if (window.innerWidth < 768) {
    viewMode.value = 'card';
  } else {
    viewMode.value = 'table';
  }
};

const fetchTeams = async (query = '') => {
  isLoading.value = true;
  try {
    const response = await axios.get(`${baseURL}/api/teams/active`, {
      params: { q: query }
    });
    // Menyesuaikan dengan struktur ProjectView.vue
    teams.value = response.data.items || response.data; 
  } catch (error) {
    toast.error("Gagal memuat data tim.");
    console.error("Gagal mengambil data tim:", error);
  } finally {
    isLoading.value = false;
  }
};

watch(searchQuery, (newQuery) => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetchTeams(newQuery);
  }, 300);
});

onMounted(() => {
  updateViewMode();
  window.addEventListener('resize', updateViewMode);
  fetchTeams();
});

const handleTeamSubmit = async (formData) => {
  try {
    await axios.post(`${baseURL}/api/teams`, formData);
    toast.success("Tim berhasil dibuat!");
    closeModal();
    await fetchTeams();
  } catch (error) {
    // Menangani error dari API dengan pesan yang lebih spesifik, seperti di ProjectView.vue
    const errorMsg = error.response?.data?.detail?.[0]?.msg || "Gagal menyimpan. Periksa kembali isian Anda.";
    toast.error(errorMsg);
    console.error("Gagal menyimpan Tim:", error.response?.data || error.message);
  }
};

const openModal = () => { isModalOpen.value = true; };
const closeModal = () => { isModalOpen.value = false; };
</script>