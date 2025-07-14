<template>
  <form @submit.prevent="handleSubmit">
    <div class="space-y-4">
      <div>
        <label for="nama-aktivitas" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nama Aktivitas</label>
        <input 
          type="text" 
          id="nama-aktivitas" 
          v-model="form.nama"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
          placeholder="Contoh: Rapat Evaluasi Bulanan"
        />
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
          v-model="form.tim"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        >
          <option disabled value="">Pilih tim</option>
          <option>Tim Neraca</option>
          <option>Tim SUTAS</option>
          <option>Divisi IT</option>
          <option>Tim Statistik Harga</option>
        </select>
      </div>

      <div>
        <label for="tanggal" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tanggal Pelaksanaan</label>
        <input 
          type="date" 
          id="tanggal" 
          v-model="form.tanggal"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        />
      </div>
    </div>

    <div class="mt-6 flex justify-end gap-3">
      <button 
        type="button" 
        @click="$emit('close')"
        class="px-4 py-2 text-sm font-medium text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none"
      >
        Batal
      </button>
      <button 
        type="submit"
        class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none"
      >
        Simpan Aktivitas
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue';

// Mendefinisikan event yang akan dipancarkan oleh komponen ini
const emit = defineEmits(['close', 'submit']);

// Menggunakan 'reactive' untuk menampung semua data form
const form = reactive({
  nama: '',
  deskripsi: '',
  tim: '',
  tanggal: '',
});

// Fungsi yang akan dijalankan saat form di-submit
const handleSubmit = () => {
  // Nanti, di sini kita akan mengirim data ke API backend.
  // Untuk sekarang, kita hanya akan memancarkan data ke parent.
  console.log('Data Form:', form);
  emit('submit', form);
  emit('close'); // Tutup modal setelah submit
};
</script>