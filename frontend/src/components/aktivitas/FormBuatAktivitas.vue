<template>
  <form @submit.prevent="handleSubmit">
    <div class="space-y-4">
      
      <div>
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
        <label for="tim" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tim Penyelenggara</label>
        <select 
          id="tim" 
          v-model="form.timPenyelenggara"
          :class="{ 'border-red-500': errors.timPenyelenggara }"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        >
          <option disabled value="">Pilih tim</option>
          <option>Tim Neraca</option>
          <option>Tim SUTAS</option>
          <option>Divisi IT</option>
          <option>Tim Statistik Harga</option>
        </select>
        <p v-if="errors.timPenyelenggara" class="mt-1 text-xs text-red-500">{{ errors.timPenyelenggara }}</p>
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
        Simpan Aktivitas
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, ref, watch } from 'vue';

const props = defineProps({
  initialData: {
    type: Object,
    default: null
  }
});
  
const emit = defineEmits(['close', 'submit']);

// State untuk form (struktur sudah benar)
const form = reactive({
  namaAktivitas: '',
  deskripsi: '',
  timPenyelenggara: '',
  useDateRange: false,
  useTime: false,
  tanggalMulai: '',
  tanggalSelesai: '',
  jamMulai: '',
  jamSelesai: '',
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
  // Reset form setiap kali modal dibuka/data berubah
  Object.assign(form, {
    namaAktivitas: '', deskripsi: '', timPenyelenggara: '', useDateRange: false,
    useTime: false, tanggalMulai: '', tanggalSelesai: '', jamMulai: '', jamSelesai: '',
  });
  daftarDokumenWajib.value = [];

  if (newData) {
    form.namaAktivitas = newData.namaAktivitas || '';
    form.deskripsi = newData.deskripsi || '';
    form.timPenyelenggara = newData.timPenyelenggara || '';
    
    const isRange = !!newData.tanggalSelesai;
    form.useDateRange = isRange;
    form.tanggalMulai = newData.tanggalMulai?.split('T')[0] || '';
    form.tanggalSelesai = isRange ? newData.tanggalSelesai?.split('T')[0] || '' : '';

    form.useTime = !!newData.jamMulai;
    form.jamMulai = newData.jamMulai || '';
    form.jamSelesai = newData.jamSelesai || '';
    daftarDokumenWajib.value = newData.daftarDokumenWajib?.map(d => d.namaDokumen) || [];

  }
}, { immediate: true, deep: true });

// Membersihkan tanggalSelesai (sudah benar)
watch(() => form.useDateRange, (isRange) => {
  if (!isRange) {
    form.tanggalSelesai = '';
  }
});

const errors = reactive({
  namaAktivitas: null,
  timPenyelenggara: null,
  tanggalMulai: null,
  tanggalSelesai: null,
  jamMulai: null,
  jamSelesai: null,
});

const validate = () => {
  Object.keys(errors).forEach(key => errors[key] = null);
  let isValid = true;
  console.log(form);

  if (!form.namaAktivitas) { errors.namaAktivitas = 'Wajib diisi.'; isValid = false; }
  if (!form.timPenyelenggara) { errors.timPenyelenggara = 'Wajib dipilih.'; isValid = false; }
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
    emit('submit', { ...form, daftarDokumenWajib: daftarDokumenWajib.value });
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