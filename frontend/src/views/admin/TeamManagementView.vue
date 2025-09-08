<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Manajemen Tim</h1>
        <div class="mt-4 relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
          </div>
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="Cari nama tim..."
            class="block w-full sm:w-80 pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-blue-500"
          />
        </div>
      </div>
      <button @click="openCreateModal" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700">
        + Tambah Tim
      </button>
    </div>

    <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <th scope="col" class="px-6 py-3 w-16">No</th>
            <th scope="col" class="px-6 py-3">Nama Tim</th>
            <th scope="col" class="px-6 py-3">Ketua Tim</th>
            <th scope="col" class="px-6 py-3">Periode Aktif</th>
            <th scope="col" class="px-6 py-3">
              <span class="sr-only">Aksi</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="teams.length === 0">
            <td colspan="4" class="px-6 py-4 text-center text-gray-500">Belum ada tim yang dibuat.</td>
          </tr>
          <tr v-for="(team, index) in teams" :key="team.id" class="border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 cursor-pointer transition-colors">
            <td class="px-6 py-4 text-center">{{ index + 1 }}</td>
            <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">{{ team.namaTim }}</th>
            <td class="px-6 py-4">
              {{ team.ketuaTim?.namaLengkap || '-' }}
            </td>
            <td class="px-6 py-4">{{ formatPeriode(team.validFrom, team.validUntil) }}</td>
            <td class="px-6 py-4 text-right">
              <button @click="openDetailModal(team)" class="p-2 rounded-full text-gray-500 hover:bg-blue-100 hover:text-blue-600 dark:hover:bg-blue-900/50 transition-colors">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                </button>
              <button v-if="authStore.isSuperAdmin"  @click="confirmDeleteTeam(team)" class="p-2 rounded-full text-gray-500 hover:bg-red-100 hover:text-red-600 dark:hover:bg-red-900/50">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <Pagination
        v-if="totalTeams > 0"
        :current-page="currentPage"
        :total-items="totalTeams"
        :items-per-page="itemsPerPage"
        @page-changed="handlePageChange"
      />

    <ModalWrapper :show="isModalOpen" @close="closeModal" :title="modalTitle">
      <FormTim
        v-if="!isEditMode"
        :user-list="allUsers"
        @close="closeModal" 
        @submit="handleTeamCreate" 
      />
      <TeamDetailModal
          v-if="isEditMode && selectedTeam"
          :team="selectedTeam"
          :user-list="allUsers"
          @close="closeModal"
          @teamUpdated="handleTeamUpdate"
      />
    </ModalWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormTim from '@/components/admin/FormTim.vue';
import TeamDetailModal from '@/components/admin/TeamDetailModal.vue';
import Pagination from '@/components/Pagination.vue';
import { useAuthStore } from '@/stores/auth';

const baseURL = import.meta.env.VITE_API_BASE_URL;
const authStore = useAuthStore();
const toast = useToast();
const teams = ref([]);
const allUsers = ref([]);
const isLoading = ref(true);
const isModalOpen = ref(false);
const isEditMode = ref(false);
const selectedTeam = ref(null);
const currentPage = ref(1);
const itemsPerPage = ref(10);
const totalTeams = ref(0);
const searchQuery = ref('');
let debounceTimer = null;

const modalTitle = computed(() => {
    if (isEditMode.value && selectedTeam.value) {
    return `Kelola Tim: ${selectedTeam.value.namaTim}`;
  }
  return 'Tambah Tim Baru';
});

const fetchData = async () => {
  isLoading.value = true;
  try {
    // Ambil data tim dan data semua pengguna secara bersamaan
    const skip = (currentPage.value - 1) * itemsPerPage.value;
    const [teamsRes, usersRes] = await Promise.all([
      axios.get(`${baseURL}/api/teams`, {
        params: { 
          skip: skip, 
          limit: itemsPerPage.value, 
          search: searchQuery.value }
      }),
      axios.get(`${baseURL}/api/users`, { params: { limit: 10000 } }) 
    ]);

    teams.value = teamsRes.data.items;
    totalTeams.value = teamsRes.data.total;
    allUsers.value = usersRes.data.items;

  } catch (error) {
    toast.error("Gagal memuat data administrasi.");
    console.error("Gagal mengambil data:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => { fetchData(); });

watch(searchQuery, () => {
  currentPage.value = 1;
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    fetchData();
  }, 500);
});

const handlePageChange = (newPage) => {
  currentPage.value = newPage;
  fetchData();
};

const formatPeriode = (start, end) => {
  const options = { day: 'numeric', month: 'short', year: 'numeric' };
  const startDate = start ? new Date(start).toLocaleDateString('id-ID', options) : '...';
  const endDate = end ? new Date(end).toLocaleDateString('id-ID', options) : '...';
  return `${startDate} - ${endDate}`;
};

const openCreateModal = () => {
    isEditMode.value = false;
    selectedTeam.value = null;
    isModalOpen.value = true;
};

const openDetailModal = (team) => {
    isEditMode.value = true;
    selectedTeam.value = team;
    isModalOpen.value = true;
};

const closeModal = () => {
    isModalOpen.value = false;
    selectedTeam.value = null;
    isEditMode.value = false; 
};

const handleTeamCreate = async (formData) => {
  try {
    await axios.post(`${baseURL}/api/teams`, formData);
    toast.success(`Tim "${formData.namaTim}" berhasil dibuat.`);
    closeModal();
    await fetchData();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Gagal membuat tim.");
  }
};


const handleTeamUpdate = async (formData) => {
    try {
      console.log('Data : ', formData);
        await axios.put(`http://127.0.0.1:8000/api/teams/${formData.id}`, formData);
        toast.success(`Tim "${formData.namaTim}" berhasil diperbarui.`);
        closeModal();
        await fetchData();
    } catch (error) {
        toast.error(error.response?.data?.detail || "Gagal memperbarui tim.");
    }
};

const confirmDeleteTeam = (team) => {
  if (window.confirm(`Apakah Anda yakin ingin menghapus tim "${team.namaTim}"?`)) {
    deleteTeam(team.id);
  }
};

const deleteTeam = async (teamId) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/teams/${teamId}`);
    toast.success("Tim berhasil dihapus.");
    await fetchData();
  } catch (error) {
    toast.error(error.response?.data?.detail || error.message);
  }
};
</script>