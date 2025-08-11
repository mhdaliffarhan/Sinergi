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
              <button @click="openEditModal(user)" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Edit</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

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
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormUser from '@/components/admin/FormUser.vue';

const toast = useToast();
const users = ref([]);
const isModalOpen = ref(false);
const sistemRoles = ref([]);
const jabatanList = ref([]);
const isEditMode = ref(false);
const userToEdit = ref(null);

const modalTitle = computed(() => isEditMode.value ? 'Edit Pengguna' : 'Tambah Pengguna Baru');

const fetchData = async () => {
  try {
    const [usersRes, rolesRes, jabatanRes] = await Promise.all([
      axios.get('http://127.0.0.1:8000/api/users'),
      axios.get('http://127.0.0.1:8000/api/sistem-roles'),
      axios.get('http://127.0.0.1:8000/api/jabatan')
    ]);
    users.value = usersRes.data;
    sistemRoles.value = rolesRes.data;
    jabatanList.value = jabatanRes.data;
  } catch (error) {
    toast.error("Gagal memuat data administrasi.");
    console.error("Gagal mengambil data:", error);
  }
};

onMounted(() => {
  fetchData();
});

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
      await axios.put(`http://127.0.0.1:8000/api/users/${userToEdit.value.id}`, payload);
      toast.success(`Pengguna "${payload.username}" berhasil diperbarui.`);
    } else {
      await axios.post('http://127.0.0.1:8000/api/users', payload);
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