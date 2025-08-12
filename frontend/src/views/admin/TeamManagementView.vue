<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Manajemen Tim</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Buat, edit, dan kelola tim di dalam sistem.</p>
      </div>
      <button @click="openCreateModal" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700">
        + Tambah Tim
      </button>
    </div>

    <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <th scope="col" class="px-6 py-3">ID Tim</th>
            <th scope="col" class="px-6 py-3">Nama Tim</th>
            <th scope="col" class="px-6 py-3">Periode Aktif</th>
            <th scope="col" class="px-6 py-3">
              <span class="sr-only">Aksi</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="isLoading">
            <td colspan="4" class="px-6 py-4 text-center text-gray-500">Memuat data tim...</td>
          </tr>
          <tr v-else-if="teams.length === 0">
            <td colspan="4" class="px-6 py-4 text-center text-gray-500">Belum ada tim yang dibuat.</td>
          </tr>
          <tr v-for="team in teams" :key="team.id" class="border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 cursor-pointer transition-colors">
            <td class="px-6 py-4">{{ team.id }}</td>
            <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">{{ team.namaTim }}</th>
            <td class="px-6 py-4">{{ formatPeriode(team.validFrom, team.validUntil) }}</td>
            <td class="px-6 py-4 text-right">
              <button @click="openDetailModal(team)" class="ml-4 font-medium text-blue-600 dark:text-blue-500 hover:underline">Detail</button>
              <button @click="confirmDeleteTeam(team)" class="p-2 rounded-full text-gray-500 hover:bg-red-100 hover:text-red-600 dark:hover:bg-red-900/50">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <ModalWrapper :show="isModalOpen" @close="closeModal" :title="modalTitle">
      <FormTim
          v-if="!isEditMode"
          @close="closeModal"
          @submit="handleTeamCreate"
      />
      <TeamDetailModal
          v-if="isEditMode && selectedTeam"
          :team="selectedTeam"
          @close="closeModal"
          @teamUpdated="handleTeamUpdate"
      />
    </ModalWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormTim from '@/components/admin/FormTim.vue';
import TeamDetailModal from '@/components/admin/TeamDetailModal.vue';

const toast = useToast();
const teams = ref([]);
const isLoading = ref(true);
const isModalOpen = ref(false);
const isEditMode = ref(false);
const selectedTeam = ref(null);
const modalTitle = computed(() => {
    return isEditMode.value ? `Kelola Tim: ${selectedTeam.value.namaTim}` : 'Tambah Tim Baru';
});

const fetchTeams = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/teams');
    teams.value = response.data;
  } catch (error) {
    toast.error("Gagal memuat data tim.");
    console.error("Gagal mengambil data tim:", error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchTeams();
});

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
const handleTeamCreate = async (formData) => {
  try {
    await axios.post('http://127.0.0.1:8000/api/teams', formData);
    toast.success(`Tim "${formData.namaTim}" berhasil dibuat.`);
    closeCreateModal();
    await fetchTeams();
  } catch (error) {
    toast.error(error.response?.data?.detail || "Gagal membuat tim.");
  }
};
const handleTeamUpdate = async (formData) => {
    try {
        await axios.put(`http://127.0.0.1:8000/api/teams/${formData.id}`, formData);
        toast.success(`Tim "${formData.namaTim}" berhasil diperbarui.`);
        closeModal();
        await fetchTeams();
    } catch (error) {
        toast.error(error.response?.data?.detail || "Gagal memperbarui tim.");
    }
};
const openDetailModal = (team) => {
    isEditMode.value = true;
    selectedTeam.value = team;
    isModalOpen.value = true;
};
const closeModal = () => {
    isModalOpen.value = false;
    selectedTeam.value = null; // Clear the selected team when closing
    isEditMode.value = false; 
};


// --- Logika untuk HAPUS ---
const confirmDeleteTeam = (team) => {
  if (window.confirm(`Apakah Anda yakin ingin menghapus tim "${team.namaTim}"?`)) {
    deleteTeam(team.id);
  }
};
const deleteTeam = async (teamId) => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/teams/${teamId}`);
    toast.success("Tim berhasil dihapus.");
    await fetchTeams();
  } catch (error) {
    toast.error("Gagal menghapus tim.");
  }
};
</script>