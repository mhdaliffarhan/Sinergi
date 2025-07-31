<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Manajemen Pengguna</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Buat, edit, dan kelola pengguna sistem.</p>
      </div>
      <button @click="openCreateModal" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg shadow-md hover:bg-blue-700">
        + Tambah Pengguna
      </button>
    </div>

    <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
      <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
        </table>
    </div>

    <ModalWrapper :show="isModalOpen" @close="closeModal" title="Tambah Pengguna Baru">
      <FormUser
        :is-edit-mode="false"
        :sistem-roles="sistemRoles"
        :jabatan-list="jabatanList"
        @close="closeModal"
        @submit="handleUserSubmit"
    />
    </ModalWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'vue-toastification';

import ModalWrapper from '@/components/ModalWrapper.vue';
import FormUser from '@/components/admin/FormUser.vue';

const authStore = useAuthStore();
const toast = useToast();
const users = ref([]);

// State untuk modal
const isModalOpen = ref(false);

// State untuk menampung data dropdown
const sistemRoles = ref([]);
const jabatanList = ref([]);

// Fungsi untuk mengambil semua data yang dibutuhkan halaman ini
const fetchData = async () => {
  try {
    // Ambil daftar pengguna
    const usersResponse = await axios.get('http://127.0.0.1:8000/api/users');
    users.value = usersResponse.data;
    // Ambil daftar peran sistem
    const rolesResponse = await axios.get('http://127.0.0.1:8000/api/sistem-roles');
    sistemRoles.value = rolesResponse.data;

    // Ambil daftar jabatan
    const jabatanResponse = await axios.get('http://127.0.0.1:8000/api/jabatan');
    jabatanList.value = jabatanResponse.data;
    toast.success("Berhasil memuat data pengguna.");
  } catch (error) {
    toast.error("Gagal memuat data pengguna.");
    console.error("Gagal mengambil data:", error);
  }
};

// Panggil fetchData saat komponen dimuat
onMounted(() => {
  fetchData();
});

// Fungsi untuk mengelola modal
const openCreateModal = () => { isModalOpen.value = true; };
const closeModal = () => { isModalOpen.value = false; };

// Fungsi untuk mengirim data user baru ke backend
const handleUserSubmit = async (formData) => {
  try {
    await axios.post('http://127.0.0.1:8000/api/users', formData);
    toast.success(`Pengguna "${formData.username}" berhasil dibuat.`);
    closeModal();
    await fetchData(); // Muat ulang data untuk menampilkan pengguna baru
  } catch (error) {
    const errorMsg = error.response?.data?.detail || "Gagal membuat pengguna.";
    toast.error(errorMsg);
    console.error(error);
  }
};

// Fungsi untuk styling badge (tidak berubah)
const getRoleClass = (roleName) => {
  if (roleName === 'Superadmin') return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
  if (roleName === 'Admin') return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
  return 'bg-gray-100 text-gray-800 dark:bg-gray-600 dark:text-gray-300';
};
</script>