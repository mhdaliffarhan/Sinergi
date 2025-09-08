<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-green-700 dark:text-green-500">Daftar Aktivitas</h1>
        <div class="mt-4 relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
          </div>
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="Cari aktivitas, deskripsi, tim, atau nama dokumen..."
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
        
        <button  @click="openModal" class="flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 transition-colors">
          <span>+</span>
          <span>Buat Baru</span>
        </button>
      </div>
    </div>

    <div class="mt-6">
      <DaftarAktivitas v-if="viewMode === 'card'" :aktivitas="aktivitas" />
      <TabelAktivitas v-if="viewMode === 'table'" :aktivitas="aktivitas" />
    </div>

    <ModalWrapper :show="isModalOpen" @close="closeModal" title="Buat Aktivitas Baru">
      <FormAktivitas @close="closeModal" @submit="handleActivitySubmit" tipe="Buat" :team-list="teamList" :project-list="projectList" :team-members="teamMembers"/>
    </ModalWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { useAuthStore } from '@/stores/auth';

import DaftarAktivitas from '@/components/aktivitas/DaftarAktivitas.vue';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormAktivitas from '@/components/aktivitas/FormAktivitas.vue';
import TabelAktivitas from '@/components/aktivitas/TabelAktivitas.vue';

const baseURL = import.meta.env.VITE_API_BASE_URL;
const authStore = useAuthStore();
const toast = useToast();
const aktivitas = ref([]);
const teamList = ref([]);
const teamMembers = ref([]);
const projectList = ref([]);
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

const fetchAktivitas = async (query = '') => {
   isLoading.value = true;
  try {
    const response = await axios.get(`${baseURL}/api/aktivitas`, {
      params: { q: query }
    });
    aktivitas.value = response.data;
    console.log("data aktivitas: ", response.data);
  } catch (error) {
    toast.error("Gagal memuat data aktivitas.");
    console.error("Gagal mengambil data aktivitas:", error);
  } finally {
    isLoading.value = false;
  }
};

const fetchTeams = async () => {
  try {
    const response = await axios.get(`${baseURL}/api/teams/active`);
    teamList.value = response.data.map(team => ({
      id: team.id,
      namaTim: team.namaTim 
    }));
     // Perulangan untuk mengambil data user di setiap tim
    for (const team of response.data) {
      if (team.users && team.users.length > 0) {
        teamMembers.value[team.id] = team.users.map(user => ({
          id: user.id,
          namaLengkap: user.namaLengkap,
          username: user.username
        }));
      }
    }
    console.log("Team list :", authStore.user);
  } catch (error) {
    toast.error("Gagal memuat daftar tim.");
    console.error("Gagal mengambil data tim:", error);
  }
};

const fetchProjects = async () => {
  try {
    const response = await axios.get(`${baseURL}/api/projects`);
    projectList.value = response.data.items.map(project => ({
      id: project.id,
      namaProject: project.namaProject,
      teamId: project.teamId,
      projectLeaderId: project.projectLeaderId
    }));
    console.log("Project : ", projectList.value);
  } catch (error) {
    toast.error("Gagal memuat data project");
    console.error("Gagal memuat data project: ", error);
  }
}

watch(searchQuery, (newQuery) => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetchAktivitas(newQuery);
  }, 300);
});

onMounted(() => {
  updateViewMode();
  window.addEventListener('resize', updateViewMode);
  fetchAktivitas();
  fetchTeams();
  fetchProjects();
});

// --- FUNGSI SUBMIT YANG MENGGABUNGKAN SEMUANYA ---
const handleActivitySubmit = async (formData) => {
  const payload = { ...formData };
  const nullableFields = ['tanggal', 'tanggalMulai', 'tanggalSelesai', 'jamMulai', 'jamSelesai'];

  // Loop melalui setiap field dan ubah nilainya jika kosong
  nullableFields.forEach(field => {
    if (payload[field] === '') {
      payload[field] = null;
    }
  });
  
  try {
    console.log("Form buat aktivitas : ", payload);
    await axios.post(`${baseURL}/api/aktivitas`, payload);
    toast.success("Aktivitas berhasil dibuat!");
    closeModal();
    await fetchAktivitas();

  } catch (error) {
    const errorMsg = error.response?.data?.detail?.[0]?.msg || "Gagal menyimpan. Periksa kembali isian Anda.";
    toast.error(errorMsg);
    console.error("Gagal menyimpan aktivitas:", error.response?.data || error.message);
  }
};

const openModal = () => { isModalOpen.value = true; };
const closeModal = () => { isModalOpen.value = false; };
</script>