<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Manajemen Pengguna</h1>
        <div class="mt-4 relative">
          <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
          </div>
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="Cari berdasarkan nama atau username..."
            class="block w-full sm:w-80 pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md leading-5 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
      </div>
      <div>
        <button @click="openCreateModal" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700">
          + Tambah Pengguna
        </button>
      </div>
      
    </div>

    <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
          <tr>
            <th scope="col" class="px-6 py-3">Nama Lengkap</th>
            <th scope="col" class="px-6 py-3">Username</th>
            <th scope="col" class="px-6 py-3">Jabatan</th>
            <th scope="col" class="px-6 py-3">Peran Sistem</th>
            <th scope="col" class="px-6 py-3">Status</th>
            <th scope="col" class="px-6 py-3"><span class="sr-only">Aksi</span></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id" class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 cursor-pointer">
            <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">{{ user.namaLengkap }}</th>
            <td class="px-6 py-4">{{ user.username }}</td>
            <td class="px-6 py-4">{{ user.jabatan?.namaJabatan || '-' }}</td>
            <td class="px-6 py-4">
              <span v-if="user.sistemRole" class="px-2 py-1 text-xs font-semibold rounded-full" :class="getRoleClass(user.sistemRole.namaRole)">
                {{ user.sistemRole.namaRole }}
              </span>
            </td>
            <td class="px-6 py-4">
              <span :class="user.isActive ? 'text-green-500' : 'text-red-500'">{{ user.isActive ? 'Aktif' : 'Non-Aktif' }}</span>
            </td>
            <td class="px-6 py-4 text-right">
               <button @click="openEditModal(user)" class="p-2 rounded-full text-gray-500 hover:bg-blue-100 hover:text-blue-600 dark:hover:bg-blue-900/50 transition-colors">
                  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg>
                </button>
              <button v-if="authStore.isSuperAdmin" @click="confirmDeleteUser(user)" class="p-2 rounded-full text-gray-500 hover:bg-red-100 hover:text-red-600 dark:hover:bg-red-900/50">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <Pagination
        v-if="totalUsers > 0"
        :current-page="currentPage"
        :total-items="totalUsers"
        :items-per-page="itemsPerPage"
        @page-changed="handlePageChange"
      />

    <ModalWrapper :show="isModalOpen" @close="closeModal" :title="modalTitle">
      <FormUser
        :is-edit-mode="isEditMode"
        :initial-data="userToEdit"
        :sistem-roles="sistemRoles"
        :jabatan-list="jabatanList"
        @close="closeModal"
        @submit="handleUserSubmit"
      />
    </ModalWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormUser from '@/components/admin/FormUser.vue';
import Pagination from '@/components/Pagination.vue';
import { useAuthStore } from '@/stores/auth';

const baseURL = import.meta.env.VITE_API_BASE_URL;
const authStore = useAuthStore();
const toast = useToast();
const users = ref([]);
const isModalOpen = ref(false);
const sistemRoles = ref([]);
const jabatanList = ref([]);
const isEditMode = ref(false);
const userToEdit = ref(null);
const currentPage = ref(1);
const itemsPerPage = ref(10);
const totalUsers = ref(0);
const searchQuery = ref('');
let debounceTimer = null;

const modalTitle = computed(() => isEditMode.value ? 'Edit Pengguna' : 'Tambah Pengguna Baru');

const fetchData = async () => {
  try {
    // Hitung 'skip' berdasarkan halaman saat ini
    const skip = (currentPage.value - 1) * itemsPerPage.value;

    // Ambil data pengguna dengan parameter skip & limit
    const usersResponse = await axios.get(`${baseURL}/api/users`, {
      params: {
        skip: skip,
        limit: itemsPerPage.value,
        search: searchQuery.value
      }
    });
    users.value = usersResponse.data.items;
    totalUsers.value = usersResponse.data.total;

    // Ambil data peran dan jabatan (hanya jika belum ada)
    if (sistemRoles.value.length === 0) {
      const rolesResponse = await axios.get('`${baseURL}/api/sistem-roles');
      sistemRoles.value = rolesResponse.data;
    }
    if (jabatanList.value.length === 0) {
      const jabatanResponse = await axios.get('`${baseURL}/api/jabatan');
      jabatanList.value = jabatanResponse.data;
    }
  } catch (error) {
    toast.error("Gagal memuat data administrasi.");
    console.error("Gagal mengambil data:", error);
  }
};

watch(searchQuery, (newQuery) => {
  // Reset ke halaman pertama setiap kali pencarian baru
  currentPage.value = 1; 
  // Hapus timer yang ada untuk mencegah request berlebihan
  clearTimeout(debounceTimer);
  // Atur timer baru. API hanya akan dipanggil setelah pengguna berhenti mengetik selama 500ms
  debounceTimer = setTimeout(() => {
    fetchData();
  }, 500);
});

onMounted(() => {
  fetchData();
});

const handlePageChange = (newPage) => {
  currentPage.value = newPage;
  fetchData(); // Ambil data untuk halaman baru
};

const openCreateModal = () => {
  isEditMode.value = false;
  userToEdit.value = null;
  isModalOpen.value = true;
};

const openEditModal = (user) => {
  isEditMode.value = true;
  userToEdit.value = user;
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  userToEdit.value = null;
};

const deleteUser = async (userId, username) => {
  try {
    await axios.delete(`${baseURL}/api/users/${userId}`);
    toast.success(`Pengguna "${username}" berhasil dihapus.`);
    await fetchData();
  } catch (error) {
    const errorMsg = error.response?.data?.detail || "Gagal menghapus pengguna.";
    toast.error(errorMsg);
    console.error(error);
  }
};

const confirmDeleteUser = (user) => {
  if (window.confirm(`Apakah Anda yakin ingin menghapus pengguna "${user.username}"? Tindakan ini tidak dapat dibatalkan.`)) {
    closeModal();
    deleteUser(user.id, user.username);
  }
};

const handleUserSubmit = async (formData) => {
  const payload = {
    username: formData.username,
    namaLengkap: formData.namaLengkap,
    sistemRoleId: formData.sistemRoleId,
    jabatanId: formData.jabatanId,
  };
  if (!isEditMode.value) {
    payload.password = formData.password;
  }

  try {
    if (isEditMode.value) {
      console.log('Data :', payload);
      await axios.put(`${baseURL}/api/users/${userToEdit.value.id}`, payload);
      toast.success(`Pengguna "${payload.username}" berhasil diperbarui.`);
    } else {
      await axios.post(`${baseURL}/api/users`, payload);
      toast.success(`Pengguna "${payload.username}" berhasil dibuat.`);
    }
    closeModal();
    await fetchData();
  } catch (error) {
    const errorMsg = error.response?.data?.detail || "Terjadi kesalahan.";
    toast.error(errorMsg);
  }
};

const getRoleClass = (roleName) => {
  if (roleName === 'Superadmin') return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
  if (roleName === 'Admin') return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
  return 'bg-gray-100 text-gray-800 dark:bg-gray-600 dark:text-gray-300';
};
</script>