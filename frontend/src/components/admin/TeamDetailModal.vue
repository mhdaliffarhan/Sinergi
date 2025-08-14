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
          :is-edit-mode="true"
        />
      </div>

      <div v-if="activeTab === 'anggota'">
        <div class="grid grid-cols-2 gap-4">
          <div>
            <h4 class="font-semibold mb-2">Anggota Tim</h4>
            <div class="border rounded-md h-96 overflow-y-auto p-2 space-y-2 dark:border-gray-600">
              <div v-for="member in teamMembers" :key="member.id" class="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700 rounded">
                <span class="text-sm">{{ member.namaLengkap }}</span>
                <button @click="removeMember(member)" class="p-1 text-red-500 hover:bg-red-100 rounded-full">
                  &times;
                </button>
              </div>
              <p v-if="teamMembers.length === 0" class="text-sm text-center text-gray-400 mt-4">Belum ada anggota.</p>
            </div>
          </div>
          <div>
            <h4 class="font-semibold mb-2">Daftar Pengguna</h4>
            <div class="border rounded-md h-96 overflow-y-auto p-2 space-y-2 dark:border-gray-600">
              <div v-for="user in availableUsers" :key="user.id" class="flex items-center justify-between p-2 hover:bg-gray-50 dark:hover:bg-gray-700 rounded">
                <span class="text-sm">{{ user.namaLengkap }}</span>
                <button @click="addMember(user)" class="p-1 text-green-500 hover:bg-green-100 rounded-full">
                  +
                </button>
              </div>
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

const emit = defineEmits(['close', 'teamUpdated']);
const toast = useToast();

const activeTab = ref('detail');
const allUsers = ref([]);
const teamMembers = ref([]);

// Ambil data detail tim (termasuk anggota) dan semua user saat komponen dimuat
const fetchData = async () => {
  try {
    const [teamDetailsRes, allUsersRes] = await Promise.all([
      axios.get(`http://127.0.0.1:8000/api/teams/${props.team.id}`),
      axios.get('http://127.0.0.1:8000/api/users', { params: { limit: 1000 } })
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
  return allUsers.value.filter(u => !memberIds.has(u.id));
});

// Fungsi untuk meneruskan update detail tim ke parent
const handleUpdate = (formData) => {
  emit('teamUpdated', { ...formData, id: props.team.id });
};

// --- LOGIKA UNTUK MENGELOLA ANGGOTA ---
const addMember = async (user) => {
  try {
    const response = await axios.post(`http://127.0.0.1:8000/api/teams/${props.team.id}/members?user_id=${user.id}`);
    teamMembers.value = response.data.users || [];
    toast.success(`"${user.namaLengkap}" berhasil ditambahkan.`);
  } catch (error) {
    toast.error("Gagal menambahkan anggota.");
  }
};

const removeMember = async (member) => {
  try {
    const response = await axios.delete(`http://127.0.0.1:8000/api/teams/${props.team.id}/members/${member.id}`);
    teamMembers.value = response.data.users || [];
    toast.success(`"${member.namaLengkap}" berhasil dikeluarkan.`);
  } catch (error) {
    toast.error("Gagal mengeluarkan anggota.");
  }
};
</script>