<template>
  <div class="flex-shrink-0 border-b border-gray-200 dark:border-gray-700">
    <nav class="flex space-x-6" aria-label="Tabs">
      <button
        @click="activeTab = 'detail'"
        :class="[activeTab === 'detail' ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:hover:text-gray-200']"
        class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
      >
        Detail Tim
      </button>
      <button
        @click="activeTab = 'anggota'"
        :class="[activeTab === 'anggota' ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:hover:text-gray-200']"
        class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
      >
        Anggota Tim
      </button>
    </nav>
  </div>

  <div class="flex-grow pt-6 overflow-y-auto">
    <div v-if="activeTab === 'detail'">
      <FormTim
        :initial-data="team"
        :user-list="props.userList"
        @submit="handleUpdate"
        @close="closeModal"
        :is-edit-mode="true"
      />
    </div>

    <div v-if="activeTab === 'anggota'">
      <div class="grid grid-cols-2 gap-4">
        <div>
          <h4 class="font-semibold mb-2 dark:text-white">Anggota Tim</h4>
          <div class="border border-gray-300 dark:border-gray-600 rounded-md h-96 overflow-y-auto p-2 space-y-2 dark:border-gray-600">
            <div v-for="member in sortedTeamMembers" :key="member.id" class="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700 rounded">
              <span class="text-sm">{{ member.namaLengkap }}</span>
              <button @click="removeMember(member)" class="p-1 text-red-500 hover:bg-red-100 dark:hover:bg-red-900/50 rounded-full">
                &times;
              </button>
            </div>
            <p v-if="teamMembers.length === 0" class="text-sm text-center text-gray-400 mt-4">Belum ada anggota.</p>
          </div>
        </div>
        <div>
          <h4 class="font-semibold mb-2 dark:text-white">Daftar Pengguna</h4>
          <div class="mb-2 relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
            </div>
            <input 
              type="text" 
              v-model="searchQuery"
              placeholder="Cari pengguna..."
              class="block w-full pl-10 pr-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-200 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
            />
          </div>
          <div class="border border-gray-300 dark:border-gray-600 rounded-md h-[22.5rem] overflow-y-auto p-2 space-y-2 dark:border-gray-600">
            <div v-for="user in availableUsers" :key="user.id" class="flex items-center justify-between p-2 hover:bg-gray-50 dark:hover:bg-gray-700 rounded cursor-pointer">
              <span class="text-sm dark:text-gray-200">{{ user.namaLengkap }}</span>
              <button @click="addMember(user)" class="p-1 text-green-500 hover:bg-green-100 dark:hover:bg-green-900/50 rounded-full">
                +
              </button>
            </div>
            <p v-if="availableUsers.length === 0 && searchQuery" class="text-sm text-center text-gray-400 mt-4">Pengguna tidak ditemukan.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import FormTim from '@/components/admin/FormTim.vue';

const props = defineProps({
  team: { type: Object, required: true },
  userList: { type: Array, required: true }
});

const baseURL = import.meta.env.VITE_API_BASE_URL;
const emit = defineEmits(['close', 'teamUpdated']);
const toast = useToast();

const activeTab = ref('detail');
const allUsers = ref([]);
const teamMembers = ref([]);
const searchQuery = ref('');

// Ambil data detail tim (termasuk anggota) dan semua user saat komponen dimuat
const fetchData = async () => {
  try {
    const [teamDetailsRes, allUsersRes] = await Promise.all([
      axios.get(`${baseURL}/api/teams/${props.team.id}`),
      axios.get(`${baseURL}/api/users`, { params: { limit: 1000 } })
    ]);
    teamMembers.value = teamDetailsRes.data.users || [];
    allUsers.value = allUsersRes.data.items || [];
  } catch (error) {
    toast.error("Gagal memuat data anggota.");
  }
};

onMounted(() => {
  fetchData();
});

// Filter daftar user agar hanya menampilkan yang BUKAN anggota tim
const availableUsers = computed(() => {
  const memberIds = new Set(teamMembers.value.map(m => m.id));
  const query = searchQuery.value.toLowerCase();

  return allUsers.value
    // 1. Filter user yang belum menjadi anggota tim
    .filter(u => !memberIds.has(u.id))
    // 2. Filter berdasarkan query pencarian (jika ada)
    .filter(u => u.namaLengkap.toLowerCase().includes(query))
    // 3. Urutkan hasilnya secara ascending (A-Z)
    .sort((a, b) => a.namaLengkap.localeCompare(b.namaLengkap));
});

const sortedTeamMembers = computed(() => {
    return [...teamMembers.value].sort((a, b) => a.namaLengkap.localeCompare(b.namaLengkap));
});

const closeModal = () => {
  emit('close');
};

// Fungsi untuk meneruskan update detail tim ke parent
const handleUpdate = (formData) => {
  emit('teamUpdated', { ...formData, id: props.team.id });
};

// --- LOGIKA UNTUK MENGELOLA ANGGOTA ---
const addMember = async (user) => {
  try {
    const response = await axios.post(`${baseURL}/api/teams/${props.team.id}/members?user_id=${user.id}`);
    teamMembers.value = response.data.users || [];
    toast.success(`"${user.namaLengkap}" berhasil ditambahkan.`);
  } catch (error) {
    toast.error("Gagal menambahkan anggota.");
  }
};

const removeMember = async (member) => {
  try {
    const response = await axios.delete(`${baseURL}/api/teams/${props.team.id}/members/${member.id}`);
    teamMembers.value = response.data.users || [];
    toast.success(`"${member.namaLengkap}" berhasil dikeluarkan.`);
  } catch (error) {
    toast.error("Gagal mengeluarkan anggota.");
  }
};
</script>