<template>
  <form @submit.prevent="handleSubmit">
    <div class="space-y-4">
      
      <div>
        <a href="">{{ project }}</a>
        <label for="nama-aktivitas" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nama Aktivitas</label>
        <input 
          type="text" 
          id="nama-aktivitas" 
          v-model="form.namaAktivitas"
          :class="{ 'border-red-500': errors.namaAktivitas }"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
          placeholder="Contoh: Rapat Evaluasi Bulanan"
        />
        <p v-if="errors.namaAktivitas" class="mt-1 text-xs text-red-500">{{ errors.namaAktivitas }}</p>
      </div>
  
      <div>
        <label for="deskripsi" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Deskripsi</label>
        <textarea 
          id="deskripsi" 
          v-model="form.deskripsi"
          rows="3"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
          placeholder="Jelaskan tujuan singkat dari aktivitas ini."
        ></textarea>
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
      <div v-if="form.teamId">
        <label for="project" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Project</label>
        <select
          id="project"
          v-model="form.projectId"
          :class="{ 'border-red-500': errors.projectId }"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        >
          <option disabled value="">Pilih project</option>
          <option
            v-for="project in filteredProjects"
            :key="project.id"
            :value="project.id"
          >
            {{ project.namaProject }}
          </option>
        </select>
        <p v-if="errors.projectId" class="mt-1 text-xs text-red-500">{{ errors.projectId }}</p>
      </div>
      
      <div v-if="form.teamId">
        <label for="anggota" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Anggota yang Terlibat
        </label>
        <div class="relative mt-1">
          <div class="block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm sm:text-sm dark:bg-gray-700 dark:text-white cursor-pointer" @click="toggleDropdown">
            <div v-if="selectedMembers.length === 0" class="text-gray-400">Pilih anggota tim...</div>
            <div v-else class="flex flex-wrap gap-2">
              <span v-for="member in selectedMembers" :key="member.id" class="inline-flex items-center rounded-full bg-blue-100 dark:bg-blue-800 px-2.5 py-0.5 text-xs font-medium text-blue-800 dark:text-blue-200">
                {{ member.namaLengkap }}
                <button type="button" @click.stop="removeMember(member.id)" class="ml-1 -mr-0.5 h-4 w-4 text-blue-500 hover:text-blue-700">
                  <svg class="h-full w-full" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                </button>
              </span>
            </div>
          </div>
          
          <div v-if="isDropdownOpen" class="absolute z-10 mt-1 w-full bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-md shadow-lg py-1 max-h-60 overflow-y-auto">
            <input type="text" v-model="searchQuery" placeholder="Cari anggota..." class="sticky top-0 w-full px-4 py-2 bg-gray-50 border-b border-gray-300 dark:border-gray-600 focus:outline-none text-sm  sm:text-sm dark:bg-gray-700 dark:text-white" @click.stop/>
            <ul class="py-1">
              <li v-for="user in filteredMembers" :key="user.id" @click="selectMember(user)" class="px-4 py-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-700  sm:text-sm dark:bg-gray-700 dark:text-white">
                <span :class="{'font-bold': isSelected(user.id)}">{{ user.namaLengkap }}</span>
              </li>
            </ul>
            <p v-if="filteredMembers.length === 0" class="text-center text-gray-400 py-4 text-sm">Tidak ada anggota ditemukan.</p>
          </div>
        </div>
      </div>

      <hr class="border-gray-200 dark:border-gray-700">
      <div>
        <label for="melibatkanKepala" class="flex items-center space-x-2 text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
          <input type="checkbox" id="melibatkanKepala" v-model="form.melibatkanKepala" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500">
          <span>Libatkan Kepala Kantor dalam aktivitas ini</span>
        </label>
      </div>

      <hr class="border-gray-200 dark:border-gray-700">

      <div class="flex items-center space-x-6">
        <label for="useDateRange" class="flex items-center space-x-2 text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
          <input type="checkbox" id="useDateRange" v-model="form.useDateRange" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500">
          <span>Gunakan rentang tanggal</span>
        </label>
        <label for="useTime" class="flex items-center space-x-2 text-sm text-gray-700 dark:text-gray-300 cursor-pointer">
          <input type="checkbox" id="useTime" v-model="form.useTime" class="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500">
          <span>Gunakan jam</span>
        </label>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="tanggal-mulai" class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            {{ form.useDateRange ? 'Tanggal Mulai' : 'Tanggal Pelaksanaan' }}
          </label>
          <input type="date" id="tanggal-mulai" v-model="form.tanggalMulai" :class="{ 'border-red-500': errors.tanggalMulai }" class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"/>
          <p v-if="errors.tanggalMulai" class="mt-1 text-xs text-red-500">{{ errors.tanggalMulai }}</p>
        </div>
        <Transition name="fade">
          <div v-if="form.useDateRange">
            <label for="tanggal-selesai" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tanggal Selesai</label>
            <input type="date" id="tanggal-selesai" v-model="form.tanggalSelesai" :class="{ 'border-red-500': errors.tanggalSelesai }" class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"/>
            <p v-if="errors.tanggalSelesai" class="mt-1 text-xs text-red-500">{{ errors.tanggalSelesai }}</p>
          </div>
        </Transition>
      </div>

      <Transition name="fade">
        <div v-if="form.useTime" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="jam-mulai" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Jam Mulai</label>
            <input type="time" id="jam-mulai" v-model="form.jamMulai" :class="{ 'border-red-500': errors.jamMulai }" class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"/>
            <p v-if="errors.jamMulai" class="mt-1 text-xs text-red-500">{{ errors.jamMulai }}</p>
          </div>
          <div>
            <label for="jam-selesai" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Jam Selesai</label>
            <input type="time" id="jam-selesai" v-model="form.jamSelesai" :class="{ 'border-red-500': errors.jamSelesai }" class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"/>
            <p v-if="errors.jamSelesai" class="mt-1 text-xs text-red-500">{{ errors.jamSelesai }}</p>
          </div>
        </div>
      </Transition>
      
      <hr class="border-gray-200 dark:border-gray-700">

      <div>
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Daftar Dokumen Wajib</label>
        <div class="flex gap-2">
          <input 
            type="text" 
            v-model="namaDokumenBaru"
            @keydown.enter.prevent="tambahDokumen"
            class="flex-grow block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
            placeholder="Contoh: Notulensi Rapat"
          />
          <button 
            type="button"
            @click="tambahDokumen"
            class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
          >
            Tambah
          </button>
        </div>
        <ul v-if="daftarDokumenWajib.length > 0" class="mt-3 space-y-2">
          <li 
            v-for="(dokumen, index) in daftarDokumenWajib" 
            :key="index"
            class="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-700/50 rounded-md"
          >
            <span class="text-sm text-gray-800 dark:text-gray-200">{{ dokumen }}</span>
            <button @click="hapusDokumen(index)" type="button" class="p-1 text-gray-400 hover:text-red-500 rounded-full">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path></svg>
            </button>
          </li>
        </ul>
      </div>
    </div>

    <div class="mt-6 flex justify-end gap-3">
      <button type="button" @click="$emit('close')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none">
        Batal
      </button>
      <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none">
        {{ tipe }} Aktivitas
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, ref, watch, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const props = defineProps({
  initialData: {
    type: Object,
    default: null
  },
  teamList: { type: Array, required: true },
  projectList: { type: Array, required: true },
  teamMembers: { type: Object, required: true },
  tipe: { type: String, required: true } 
});
  
const daftarTim = computed(() => {
  if (!props.teamList) {
    return [];
  }
  if (!authStore.user?.teams) {
    return [];
  }
  const userTeamIds = authStore.user.teams.map(team => team.id);
  
  return props.teamList.filter(tim => 
    userTeamIds.includes(tim.id)
  );
});

const filteredProjects = computed(() => {
  if (!form.teamId || !props.projectList) {
    return [];
  }
  return props.projectList.filter(project => project.teamId === form.teamId);
});

const emit = defineEmits(['close', 'submit']);

// State untuk multi-select
const isDropdownOpen = ref(false);
const searchQuery = ref('');
const selectedMembers = ref([]);

// Komputerisasi untuk anggota tim yang difilter
const filteredMembers = computed(() => {
  const members = props.teamMembers[form.teamId] || [];
  const query = searchQuery.value.toLowerCase();
  return members.filter(user =>
    user.namaLengkap.toLowerCase().includes(query) || user.username.toLowerCase().includes(query)
  );
});

// Method untuk multi-select
const toggleDropdown = () => { isDropdownOpen.value = !isDropdownOpen.value; };
const isSelected = (id) => selectedMembers.value.some(member => member.id === id);
const selectMember = (user) => {
  if (!isSelected(user.id)) {
    selectedMembers.value.push(user);
  } else {
    removeMember(user.id);
  }
};
const removeMember = (id) => {
  selectedMembers.value = selectedMembers.value.filter(member => member.id !== id);
};

const form = reactive({
  namaAktivitas: '',
  deskripsi: '',
  teamId: '',
  projectId: '',
  useDateRange: false,
  useTime: false,
  tanggalMulai: '',
  tanggalSelesai: '',
  jamMulai: '',
  jamSelesai: '',
  melibatkanKepala: false
});

const namaDokumenBaru = ref('');
const daftarDokumenWajib = ref([]);

const tambahDokumen = () => {
  if (namaDokumenBaru.value.trim()) {
    daftarDokumenWajib.value.push(namaDokumenBaru.value.trim());
    namaDokumenBaru.value = '';
  }
};

const hapusDokumen = (index) => {
  daftarDokumenWajib.value.splice(index, 1);
};

// Mengisi form saat ada initialData (lebih andal)
watch(() => props.initialData, (newData) => {
  Object.assign(form, {
    namaAktivitas: '', deskripsi: '', teamId: '', useDateRange: false,
    useTime: false, tanggalMulai: '', tanggalSelesai: '', jamMulai: '', jamSelesai: '',
  });
  daftarDokumenWajib.value = [];
  selectedMembers.value = []; // Tambahan: Reset anggota yang dipilih

  if (newData) {
    form.namaAktivitas = newData.namaAktivitas || '';
    form.deskripsi = newData.deskripsi || '';
    form.teamId = newData.teamId || '';
    form.projectId = newData.projectId || '';
    form.melibatkanKepala = newData.melibatkanKepala || false;

    const isRange = !!newData.tanggalSelesai;
    form.useDateRange = isRange;
    form.tanggalMulai = newData.tanggalMulai?.split('T')[0] || '';
    form.tanggalSelesai = isRange ? newData.tanggalSelesai?.split('T')[0] || '' : '';

    form.useTime = !!newData.jamMulai;
    form.jamMulai = newData.jamMulai || '';
    form.jamSelesai = newData.jamSelesai || '';
    daftarDokumenWajib.value = newData.daftarDokumenWajib?.map(d => d.namaDokumen) || [];
    selectedMembers.value = newData.users || []; // Tambahan: Isi anggota yang sudah ada
  }
}, { immediate: true, deep: true });

watch(() => form.teamId, (newTeamId, oldTeamId) => {
  if (newTeamId !== oldTeamId) {
    form.projectId = '';
    selectedMembers.value = [];
    isDropdownOpen.value = false;
    searchQuery.value = '';
  }
});

watch(() => form.useDateRange, (isRange) => {
  if (!isRange) {
    form.tanggalSelesai = '';
  }
});

const errors = reactive({
  namaAktivitas: null,
  teamId: null,
  projectId: null,
  tanggalMulai: null,
  tanggalSelesai: null,
  jamMulai: null,
  jamSelesai: null,
});

const validate = () => {
  Object.keys(errors).forEach(key => errors[key] = null);
  let isValid = true;

  if (!form.namaAktivitas) { errors.namaAktivitas = 'Wajib diisi.'; isValid = false; }
  if (!form.teamId) { errors.teamId = 'Wajib dipilih.'; isValid = false; }
  if (form.teamId && !form.projectId) { errors.projectId = 'Wajib dipilih.'; isValid = false; }
  
  if (!form.tanggalMulai) { errors.tanggalMulai = 'Wajib diisi.'; isValid = false; }
  
  if (form.useDateRange) {
    if (!form.tanggalSelesai) { errors.tanggalSelesai = 'Wajib diisi.'; isValid = false; }
    if (form.tanggalMulai && form.tanggalSelesai && form.tanggalSelesai < form.tanggalMulai) {
      errors.tanggalSelesai = 'Tanggal selesai tidak boleh sebelum tanggal mulai.';
      isValid = false;
    }
  }

  if (form.useTime) {
    if (!form.jamMulai) { errors.jamMulai = 'Wajib diisi.'; isValid = false; }
    if (!form.jamSelesai) { errors.jamSelesai = 'Wajib diisi.'; isValid = false; }
    
    const isSameDay = !form.useDateRange || (form.useDateRange && form.tanggalMulai === form.tanggalSelesai);
    if (form.jamMulai && form.jamSelesai && isSameDay && form.jamSelesai <= form.jamMulai) {
      errors.jamSelesai = 'Jam selesai harus setelah jam mulai (di hari yang sama).';
      isValid = false;
    }
  }
  return isValid;
};

const handleSubmit = () => {
  if (validate()) {
    const payload = {
      ...form,
      daftarDokumenWajib: daftarDokumenWajib.value,
      anggotaAktivitasIds: selectedMembers.value.map(member => member.id)
    };
    emit('submit', payload);
  }
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>