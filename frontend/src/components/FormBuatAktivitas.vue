<template>
  <form @submit.prevent="handleSubmit">
    <div class="space-y-4">
      <div>
        <label for="nama-aktivitas" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nama Aktivitas</label>
        <input 
          type="text" 
          id="nama-aktivitas" 
          v-model="form.namaAktivitas"
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
          v-model="form.timPenyelenggara"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        >
          <option disabled value="">Pilih tim</option>
          <option>Tim Neraca</option>
          <option>Tim SUTAS</option>
          <option>Divisi IT</option>
          <option>Tim Statistik Harga</option>
        </select>
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
            <label for="tanggal-mulai" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tanggal Mulai</label>
            <input type="date" id="tanggal-mulai" v-model="form.tanggalMulai" class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"/>
          </div>
          <div>
            <label for="tanggal-selesai" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tanggal Selesai</label>
            <input type="date" id="tanggal-selesai" v-model="form.tanggalSelesai" class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"/>
          </div>
        </div>
        <div v-else>
          <label for="tanggal" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Tanggal Pelaksanaan</label>
          <input type="date" id="tanggal" v-model="form.tanggalMulai" class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"/>
        </div>
      </Transition>

      <Transition name="fade">
        <div v-if="form.useTime" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label for="jam-mulai" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Jam Mulai</label>
            <input type="time" id="jam-mulai" v-model="form.jamMulai" class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"/>
          </div>
          <div>
            <label for="jam-selesai" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Jam Selesai</label>
            <input type="time" id="jam-selesai" v-model="form.jamSelesai" class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"/>
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

// Perbarui 'form' untuk menampung semua state baru
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

const handleSubmit = () => {
  console.log('Data Form:', form);
  emit('submit', form);
  emit('close');
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