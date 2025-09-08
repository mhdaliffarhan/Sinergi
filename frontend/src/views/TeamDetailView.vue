<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <svg class="animate-spin -ml-1 mr-3 h-10 w-10 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <div v-else-if="!team" class="text-center text-gray-500 dark:text-gray-400 py-10">
      Tim tidak ditemukan.
    </div>

    <div v-else>
      <div class="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
        <div class="md:mb-0">
          <p class="text-base font-semibold text-gray-500 dark:text-gray-400">Tim</p>
          <div class="flex items-center gap-2 mt-1">
            <div class="w-6 h-6 rounded-full" :style="{ backgroundColor: team.warna || '#3b82f6' }"></div>
            <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">{{ team.namaTim }}</h1>
          </div>
          <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
            Periode Aktif: {{ formatDate(team.validFrom) }} - {{ formatDate(team.validUntil) }}
          </p>
        </div>
        
        <div class="flex-shrink-0 w-full md:w-auto">
          <button v-if="isSuperadminOrKetuaTim" @click="openEditModal" class="px-4 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 transition-colors">
            Edit Tim
          </button>
        </div>
      </div>

      <section class="mt-8 bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-6">
          <div class="flex items-center gap-4">
            <span class="text-2xl">👥</span>
            <div>
              <span class="text-xl font-bold text-gray-900 dark:text-white">{{ team.users?.length ?? 0 }}</span>
              <p class="text-sm text-gray-500 dark:text-gray-400">Anggota</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <span class="text-2xl">💼</span>
            <div>
              <span class="text-xl font-bold text-gray-900 dark:text-white">{{ team.projects?.length ?? 0 }}</span>
              <p class="text-sm text-gray-500 dark:text-gray-400">Project</p>
            </div>
          </div>
          <div class="flex items-center gap-4">
            <span class="text-2xl">✅</span>
            <div>
              <span class="text-xl font-bold text-gray-900 dark:text-white">{{ totalAktivitas }}</span>
              <p class="text-sm text-gray-500 dark:text-gray-400">Aktivitas</p>
            </div>
          </div>
        </div>
        
        <hr class="my-4 border-gray-200 dark:border-gray-700">

        <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-4">Ketua Tim & Anggota</h2>
        <div v-if="team.users?.length > 0" class="flex flex-wrap items-center gap-4">
          <div v-if="team.ketuaTim" class="flex flex-col items-center">
            <div 
              class="relative h-16 w-16 rounded-full flex items-center justify-center text-base font-semibold text-gray-600 dark:text-gray-300 ring-4 ring-green-500 transition duration-150 transform hover:scale-110 hover:z-10 cursor-pointer"
              :title="team.ketuaTim.namaLengkap + ' (Ketua Tim)'"
              @click="goToUserDetail(team.ketuaTim.id)"
            >
              <img v-if="team.ketuaTim.fotoProfilUrl"
                :src="getProfileUrl(team.ketuaTim.fotoProfilUrl)"
                alt="Profil"
                class="h-full w-full rounded-full object-cover"
              />
              <div v-else
                class="h-full w-full rounded-full flex items-center justify-center text-white text-base"
                :style="{ backgroundColor: getSoftRandomColor(team.ketuaTim.id) }"
              >
                {{ getInitials(team.ketuaTim.namaLengkap) }}
              </div>
            </div>
            <p class="text-xs text-green-500 font-bold mt-2 text-center">Ketua Tim</p>
          </div>
          
          <div class="flex flex-wrap -space-x-3">
            <div 
              v-for="user in filteredUsers" 
              :key="user.id" 
              class="relative h-12 w-12 rounded-full flex items-center justify-center text-xs font-semibold text-gray-600 dark:text-gray-300 ring-2 ring-white dark:ring-gray-800 transition duration-150 transform hover:scale-110 hover:z-10 cursor-pointer"
              :title="user.namaLengkap"
              @click="goToUserDetail(user.id)"
            >
              <img v-if="user.fotoProfilUrl"
                :src="getProfileUrl(user.fotoProfilUrl)"
                alt="Profil"
                class="h-full w-full rounded-full object-cover"
              />
              <div v-else
                class="h-full w-full rounded-full flex items-center justify-center text-white"
                :style="{ backgroundColor: getSoftRandomColor(user.id) }"
              >
                {{ getInitials(user.namaLengkap) }}
              </div>
            </div>
          </div>
        </div>

        <div v-else class="text-center text-gray-500 dark:text-gray-400 p-6">
          Tidak ada anggota yang terdaftar dalam tim ini.
        </div>
      </section>

      <section class="mt-8">
        <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Proyek dan Aktivitas</h2>
        <div v-if="team.projects?.length > 0" class="space-y-6">
          <div v-for="project in team.projects" :key="project.id" class="bg-white dark:bg-gray-800 shadow-lg rounded-lg overflow-hidden">
            <div @click="toggleProject(project.id)" class="cursor-pointer p-4 sm:p-6 flex items-center justify-between transition-colors hover:bg-gray-50 dark:hover:bg-gray-700">
              <div class="flex items-center gap-4">
                <span class="text-sm font-medium text-blue-500 dark:text-blue-400">
                  {{ project.projectLeader?.namaLengkap || 'Tidak ada leader' }}
                </span>
                <router-link :to="{ name: 'project-detail', params: { id: project.id } }" class="text-lg font-bold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                  {{ project.namaProject }}
                </router-link>
              </div>
              <div class="flex items-center gap-4">
                <span class="text-sm text-gray-500 dark:text-gray-400 hidden md:inline">
                  {{ project.aktivitas?.length ?? 0 }} Aktivitas
                </span>
                <svg :class="{'rotate-180': expandedProjects[project.id]}" class="w-5 h-5 text-gray-500 transform transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
              </div>
            </div>

            <div v-show="expandedProjects[project.id]" class="p-4 sm:p-6 border-t border-gray-200 dark:border-gray-700">
              <div v-if="project.aktivitas?.length > 0">
                <div class="overflow-x-auto rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
                  <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                      <tr>
                        <th scope="col" class="px-6 py-3 w-1/2">
                          Nama Aktivitas
                        </th>
                        <th scope="col" class="px-6 py-3 text-center">
                          Jadwal Pelaksanaan
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr 
                        v-for="aktivitas in project.aktivitas" 
                        :key="aktivitas.id" 
                        @click="goToAktivitasDetail(aktivitas.id)"
                        class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 cursor-pointer transition-colors"
                      >
                        <td scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                          <div class="flex flex-col gap-1">
                            <span class="inline-flex items-center w-fit px-2 py-1 text-xs font-medium rounded-full text-white"
                              :style="{ backgroundColor: team.warna || '#3b82f6' }">
                              {{ team.namaTim || '-' }}
                            </span>
                            <span class="font-medium">
                              {{ aktivitas.namaAktivitas }}
                            </span>
                          </div>
                        </td>
                        <td class="px-6 py-4 text-center">
                          <div class="flex flex-col">
                            <span class="flex items-center gap-2">
                              <span>🗓️</span>
                              <span>{{ formatJadwal(aktivitas).tanggal }}</span>
                            </span>
                            <span v-if="formatJadwal(aktivitas).waktu" class="flex items-center gap-2 mt-1 text-xs text-gray-400">
                              <span>🕒</span>
                              <span>{{ formatJadwal(aktivitas).waktu }}</span>
                            </span>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <div v-else class="text-center text-gray-500 dark:text-gray-400">
                Project ini belum memiliki aktivitas.
              </div>
            </div>
          </div>
        </div>
        <div v-else class="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 text-center text-gray-500 dark:text-gray-400">
          Tim ini belum memiliki proyek atau aktivitas.
        </div>
      </section>

      <ModalWrapper :show="isEditModalOpen" @close="closeModal" title="Kelola Tim">
        <TeamDetailModal
          v-if="team && allUsers.length > 0"
          :team="team"
          :user-list="allUsers"
          @close="closeModal"
          @teamUpdated="handleUpdateTeamDetails"
          @addMember="addMemberToTeam"
          @removeMember="removeMemberFromTeam"
        />
      </ModalWrapper>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import { format } from 'date-fns';
import { id } from 'date-fns/locale';

import ModalWrapper from '@/components/ModalWrapper.vue';
import { useAuthStore } from '@/stores/auth';
import TeamDetailModal from '@/components/admin/TeamDetailModal.vue';

const baseURL = import.meta.env.VITE_API_BASE_URL;
const route = useRoute();
const router = useRouter();
const toast = useToast();
const authStore = useAuthStore();

const team = ref(null);
const isLoading = ref(true);
const isEditModalOpen = ref(false);
const expandedProjects = ref({});
const allUsers = ref([]);

const isSuperadminOrKetuaTim = computed(() => {
  return authStore.user?.sistemRole.namaRole === 'Superadmin' || authStore.user?.id === team.value?.ketuaTim?.id;
});

const totalAktivitas = computed(() => {
  if (!team.value || !team.value.projects) return 0;
  return team.value.projects.reduce((sum, project) => sum + (project.aktivitas?.length ?? 0), 0);
});

const filteredUsers = computed(() => {
  if (!team.value?.users) return [];
  return team.value.users.filter(user => user.id !== team.value.ketuaTim?.id);
});

const toggleProject = (projectId) => {
  expandedProjects.value[projectId] = !expandedProjects.value[projectId];
};

const goToAktivitasDetail = (id) => {
  router.push({ name: 'aktivitas-detail', params: { id } });
};

const goToUserDetail = (userId) => {
  router.push({ name: 'user-detail', params: { id: userId } });
};

const fetchTeamDetails = async () => {
  try {
    const teamId = route.params.id;
    const [teamRes, usersRes] = await Promise.all([
      axios.get(`${baseURL}/api/teams/${teamId}/details`),
      axios.get(`${baseURL}/api/users`, { params: { limit: 10000 } })
    ]);
    team.value = teamRes.data;
    allUsers.value = usersRes.data.items;
    console.log("Data tim : ", team.value);
  } catch (error) {
    toast.error("Gagal memuat detail tim.");
    console.error("Error fetching team details:", error);
  } finally {
    isLoading.value = false;
  }
};

const formatDate = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return format(date, 'd MMMM yyyy', { locale: id });
};

const formatJadwal = (item) => {
  if (!item.tanggalMulai) return { tanggal: '-', waktu: null };
  const options = { day: 'numeric', month: 'short', year: 'numeric' };
  let tanggalTampil = '';
  let waktuTampil = null;
  const tglMulai = new Date(item.tanggalMulai);
  if (item.tanggalSelesai) {
    const tglSelesai = new Date(item.tanggalSelesai);
    tanggalTampil = `${tglMulai.toLocaleDateString('id-ID', options)} - ${tglSelesai.toLocaleDateString('id-ID', options)}`;
  } else {
    tanggalTampil = tglMulai.toLocaleDateString('id-ID', options);
  }
  if (item.jamMulai) {
    const jamMulai = item.jamMulai.substring(0, 5);
    const jamSelesai = item.jamSelesai ? item.jamSelesai.substring(0, 5) : null;
    waktuTampil = `${jamMulai} - ${jamSelesai} WITA`;
  }
  return { tanggal: tanggalTampil, waktu: waktuTampil };
};

const getInitials = (name) => {
  if (!name) return '';
  const parts = name.split(' ').filter(p => p.length > 0);
  if (parts.length === 0) return '';
  const firstInitial = parts[0][0];
  const lastPart = parts[parts.length - 1];
  const lastInitial = lastPart.replace(/[^a-zA-Z]/g, '')[0];
  return (firstInitial + lastInitial).toUpperCase();
};

const getSoftRandomColor = (seed) => {
  const colors = [
    '#fbcfe8', '#fecaca', '#dbeafe', '#d1d5db', '#c7d2fe'
  ];
  return colors[seed % colors.length];
};

const openEditModal = () => { isEditModalOpen.value = true; };
const closeModal = () => { isEditModalOpen.value = false; };

// Fungsi untuk update detail tim
const handleUpdateTeamDetails = async (formData) => {
  try {
    const payload = { ...formData, id: team.value.id };
    await axios.put(`${baseURL}/api/teams/${team.value.id}`, payload);
    toast.success("Detail tim berhasil diperbarui!");
    closeModal();
    await fetchTeamDetails();
  } catch (error) {
    const errorMsg = error.response?.data?.detail?.[0]?.msg || "Gagal memperbarui detail tim.";
    toast.error(errorMsg);
    console.error("Error updating team details:", error.response?.data || error.message);
  }
};

// Fungsi untuk menambah anggota tim
const addMemberToTeam = async (user) => {
  try {
    const response = await axios.post(`${baseURL}/api/teams/${team.value.id}/members?user_id=${user.id}`);
    team.value.users = response.data.users; // Update daftar anggota
    toast.success(`"${user.namaLengkap}" berhasil ditambahkan.`);
  } catch (error) {
    toast.error("Gagal menambahkan anggota.");
  }
};

// Fungsi untuk menghapus anggota tim
const removeMemberFromTeam = async (user) => {
  try {
    const response = await axios.delete(`${baseURL}/api/teams/${team.value.id}/members/${user.id}`);
    team.value.users = response.data.users; // Update daftar anggota
    toast.success(`"${user.namaLengkap}" berhasil dikeluarkan.`);
  } catch (error) {
    toast.error("Gagal mengeluarkan anggota.");
  }
};

onMounted(() => {
  fetchTeamDetails();
});

const getProfileUrl = (path) => {
  if (!path) return "/profile-default.png";
  if (path.startsWith("./")) {
    return `${baseURL}/${path.replace("./", "")}`;
  }
  return path;
};
</script>