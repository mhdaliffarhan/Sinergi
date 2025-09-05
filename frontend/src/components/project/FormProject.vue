<template>
  <form @submit.prevent="handleSubmit">
    <div class="space-y-4">
      
      <div>
        <label for="nama-project" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nama Project</label>
        <input 
          type="text" 
          id="nama-project" 
          v-model="form.namaProject"
          :class="{ 'border-red-500': errors.namaProject }"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
          placeholder="Contoh: Aplikasi Manajemen Mitra"
        />
        <p v-if="errors.namaProject" class="mt-1 text-xs text-red-500">{{ errors.namaProject }}</p>
      </div>

      <div>
        <label for="tim" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tim</label>
        <select 
          id="tim" 
          v-model="form.teamId"
          :class="{ 'border-red-500': errors.teamId }"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        >
          <option disabled value="">Pilih tim</option>
          <option 
            v-for="tim in daftarTim" 
            :key="tim.id" 
            :value="tim.id"
          >
            {{ tim.namaTim }}
          </option>
        </select>
        <p v-if="errors.teamId" class="mt-1 text-xs text-red-500">{{ errors.teamId }}</p>
      </div>

      <div>
        <label for="project-leader" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Project Leader</label>
        <select 
          id="project-leader" 
          v-model="form.projectLeaderId"
          :class="{ 'border-red-500': errors.projectLeaderId }"
          :disabled="!form.teamId"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        >
          <option disabled value="">Pilih Project Leader</option>
          <option 
            v-for="user in teamMembers" 
            :key="user.id"  
            :value="user.id"
          >
            {{ user.namaLengkap }} ({{ user.username }})
          </option>
        </select>
        <p v-if="errors.projectLeaderId" class="mt-1 text-xs text-red-500">{{ errors.projectLeaderId }}</p>
      </div>
      
    </div>

    <div class="mt-6 flex justify-end gap-3">
      <button type="button" @click="$emit('close')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none">
        Batal
      </button>
      <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none">
        {{ tipe }} Project
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, ref, computed, watch } from 'vue';
import { useAuthStore } from '@/stores/auth';
import axios from 'axios';
import { useToast } from 'vue-toastification';

const authStore = useAuthStore();
const toast = useToast();

const props = defineProps({
  initialData: {
    type: Object,
    default: null
  },
  teamList: { type: Array, required: true },
  tipe : { type: String, required: true}
});
  
const daftarTim = computed(() => {
  if (!props.teamList) return [];
  if (!authStore.user?.ketuaTimAktif) return [];
  return props.teamList.filter(tim => 
    authStore.user.ketuaTimAktif.some(k => k.id === tim.id)
  );
});

const emit = defineEmits(['close', 'submit']);

const form = reactive({
  namaProject: '',
  teamId: '',
  projectLeaderId: null,
});

const teamMembers = ref([]);

const errors = reactive({
  namaProject: null,
  teamId: null,
  projectLeaderId: null,
});

// Watcher untuk memuat anggota tim saat teamId berubah
watch(() => form.teamId, async (newTeamId) => {
  // Atur ulang projectLeaderId saat tim berubah
  form.projectLeaderId = null; 
  teamMembers.value = [];

  if (newTeamId) {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/api/teams/${newTeamId}`);
      teamMembers.value = response.data.users;
    } catch (error) {
      toast.error("Gagal memuat anggota tim.");
      console.error("Gagal mengambil data anggota tim:", error);
    }
  }
});

// --- TAMBAHAN: Watcher untuk mengisi form saat initialData berubah ---
watch(() => props.initialData, (newData) => {
    // Reset form ke nilai default
    form.namaProject = '';
    form.teamId = '';
    form.projectLeaderId = null;
    teamMembers.value = [];

    if (newData) {
        form.namaProject = newData.namaProject || '';
        form.teamId = newData.teamId || '';
        
        // PENTING: Perlu memuat anggota tim terlebih dahulu sebelum mengisi projectLeaderId
        // Ini memastikan opsi projectLeaderId sudah tersedia di dropdown saat diisi
        // Ini akan memicu watcher form.teamId di atas
        if (newData.teamId) {
            axios.get(`http://127.0.0.1:8000/api/teams/${newData.teamId}`).then(response => {
                teamMembers.value = response.data.users;
                form.projectLeaderId = newData.projectLeaderId || null;
            });
        }
    }
}, { immediate: true }); // 'immediate: true' akan menjalankan watcher saat komponen pertama kali dimuat

const validate = () => {
  Object.keys(errors).forEach(key => errors[key] = null);
  let isValid = true;

  if (!form.namaProject) { errors.namaProject = 'Wajib diisi.'; isValid = false; }
  if (!form.teamId) { errors.teamId = 'Wajib dipilih.'; isValid = false; }
  if (!form.projectLeaderId) { errors.projectLeaderId = 'Wajib dipilih.'; isValid = false; }
  
  return isValid;
};

const handleSubmit = () => {
  if (validate()) {
    emit('submit', { 
      namaProject: form.namaProject,
      teamId: form.teamId,
      projectLeaderId: form.projectLeaderId,
    });
  }
};
</script>