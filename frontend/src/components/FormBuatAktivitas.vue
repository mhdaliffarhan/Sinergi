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

      <Transition name="fade">
        <div v-if="form.useDateRange" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="tanggal-mulai"  class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tanggal Mulai</label>
            <input type="date" id="tanggal-mulai" v-model="form.tanggalMulai" :class="{ 'border-red-500': errors.tanggalMulai }" class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"/>
            <p v-if="errors.tanggalMulai" class="mt-1 text-xs text-red-500">{{ errors.tanggalMulai }}</p>
          </div>
          <div>
            <label for="tanggal-selesai" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tanggal Selesai</label>
            <input type="date" id="tanggal-selesai" v-model="form.tanggalSelesai" :class="{ 'border-red-500': errors.tanggalSelesai }" class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"/>
            <p v-if="errors.tanggalSelesai" class="mt-1 text-xs text-red-500">{{ errors.tanggalSelesai }}</p>
          </div>
        </div>
        <div v-else>
          <label for="tanggal" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tanggal Pelaksanaan</label>
          <input type="date" id="tanggal" v-model="form.tanggalMulai" :class="{ 'border-red-500': errors.tanggalMulai }" class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"/>
          <p v-if="errors.tanggalMulai" class="mt-1 text-xs text-red-500">{{ errors.tanggalMulai }}</p>
        </div>
      </Transition>

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
import { reactive } from 'vue';

const emit = defineEmits(['close', 'submit']);

// State untuk form
const form = reactive({
  namaAktivitas: '',
  deskripsi: '',
  timPenyelenggara: '',
  tanggal: '',
  useDateRange: false,
  useTime: false,
  tanggalMulai: '',
  tanggalSelesai: '',
  jamMulai: '',
  jamSelesai: '',
});

// State untuk menampung pesan error
const errors = reactive({
  namaAktivitas: null,
  timPenyelenggara: null,
  tanggal: null,
  tanggalMulai: null,
  tanggalSelesai: null,
  jamMulai: null,
  jamSelesai: null,
});

// Fungsi validasi utama
const validate = () => {
  // Reset semua error sebelum validasi baru
  Object.keys(errors).forEach(key => errors[key] = null);
  let isValid = true;

  // Rule 1: Wajib diisi
  if (!form.namaAktivitas) {
    errors.namaAktivitas = 'Nama aktivitas wajib diisi.';
    isValid = false;
  }
  if (!form.timPenyelenggara) {
    errors.timPenyelenggara = 'Tim penyelenggara wajib dipilih.';
    isValid = false;
  }

  // Rule 2: Validasi tanggal
  if (form.useDateRange) {
    if (!form.tanggalMulai) { errors.tanggalMulai = 'Wajib diisi.'; isValid = false; }
    if (!form.tanggalSelesai) { errors.tanggalSelesai = 'Wajib diisi.'; isValid = false; }
    if (form.tanggalMulai && form.tanggalSelesai && form.tanggalSelesai < form.tanggalMulai) {
      errors.tanggalSelesai = 'Tanggal selesai tidak boleh sebelum tanggal mulai.';
      isValid = false;
    }
  } else {
    if (!form.tanggalMulai) { errors.tanggalMulai = 'Wajib diisi.'; isValid = false; }
  }

  // Rule 3: Validasi jam
  if (form.useTime) {
    if (!form.jamMulai) { errors.jamMulai = 'Wajib diisi.'; isValid = false; }
    if (!form.jamSelesai) { errors.jamSelesai = 'Wajib diisi.'; isValid = false; }
    if (form.jamMulai && form.jamSelesai && form.tanggalMulai === form.tanggalSelesai && form.jamSelesai < form.jamMulai) {
      errors.jamSelesai = 'Jam selesai tidak boleh sebelum jam mulai (di hari yang sama).';
      isValid = false;
    }
  }
  
  return isValid;
};

const handleSubmit = () => {
  if (validate()) {
    // Jika valid, kirim event submit ke parent
    emit('submit', form);
  }
  // Jika tidak valid, tidak lakukan apa-apa. Pesan error akan otomatis tampil.
};
</script>

<style scoped>
/* CSS untuk transisi fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>