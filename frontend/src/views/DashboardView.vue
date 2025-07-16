<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-green-700 dark:text-green-500">Dashboard Aktivitas</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Selamat datang kembali! Ini adalah daftar aktivitas terbaru.</p>
      </div>
      <div class="mt-4 sm:mt-0 flex items-center gap-2">
        <div class="relative inline-flex items-center bg-gray-100 dark:bg-gray-700 p-1 rounded-lg">
          <span
            class="absolute top-1 bottom-1 left-1 w-[calc(50%-0.25rem)] bg-orange-500 rounded-md shadow-md transition-transform duration-300 ease-in-out"
            :class="{ 'translate-x-full': viewMode === 'table' }"
          ></span>

          <button
            @click="viewMode = 'card'"
            class="relative z-10 w-1/2 px-3 py-1.5 flex justify-center items-center transition-colors duration-300"
            :class="viewMode === 'card' ? 'text-white' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
          </button>
          
          <button
            @click="viewMode = 'table'"
            class="relative z-10 w-1/2 px-3 py-1.5 flex justify-center items-center transition-colors duration-300"
            :class="viewMode === 'table' ? 'text-white' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path></svg>
          </button>
        </div>
        
        <button @click="openModal" class="flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 transition-colors">
          <span>+</span>
          <span>Buat Baru</span>
        </button>
      </div>
    </div>

    <div class="mt-6">
      <DaftarAktivitas v-if="viewMode === 'card'" :aktivitas="aktivitas" />
      <TabelAktivitas v-if="viewMode === 'table'" :aktivitas="aktivitas" />
    </div>

    <ModalWrapper :show="isModalOpen" @close="closeModal" title="Buat Aktivitas Baru">
      <FormBuatAktivitas @close="closeModal" @submit="handleActivitySubmit" />
    </ModalWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useToast } from 'vue-toastification';

import DaftarAktivitas from '@/components/DaftarAktivitas.vue';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormBuatAktivitas from '@/components/FormBuatAktivitas.vue';
import TabelAktivitas from '@/components/TabelAktivitas.vue';

const toast = useToast();
const aktivitas = ref([]);
const isModalOpen = ref(false);
const viewMode = ref('table');

// --- FUNGSI KONVERSI (tetap sama) ---
const snakeToCamel = (str) => str.replace(/([-_][a-z])/g, (group) => group.toUpperCase().replace('-', '').replace('_', ''));
const convertKeysToCamelCase = (obj) => {
  if (obj === null || typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map(convertKeysToCamelCase);
  
  const newObj = {};
  for (let key in obj) {
    newObj[snakeToCamel(key)] = convertKeysToCamelCase(obj[key]);
  }
  return newObj;
};

const fetchAktivitas = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/aktivitas');
    console.log(response.data);
    aktivitas.value = convertKeysToCamelCase(response.data);
  } catch (error) {
    toast.error("Gagal memuat data aktivitas.");
    console.error("Gagal mengambil data aktivitas:", error);
  }
};

onMounted(() => {
  fetchAktivitas();
});

// --- FUNGSI SUBMIT YANG MENGGABUNGKAN SEMUANYA ---
const handleActivitySubmit = async (formData) => {
  // Buat salinan data form untuk kita modifikasi
  const payload = { ...formData };

  // Daftar field yang harus diubah dari string kosong menjadi null
  const nullableFields = ['tanggal', 'tanggalMulai', 'tanggalSelesai', 'jamMulai', 'jamSelesai'];

  // Loop melalui setiap field dan ubah nilainya jika kosong
  nullableFields.forEach(field => {
    if (payload[field] === '') {
      payload[field] = null;
    }
  });

  console.log('Mengirim data yang sudah dibersihkan:', payload);
  
  try {
    // Kirim 'payload' yang sudah bersih ke backend
    await axios.post('http://127.0.0.1:8000/api/aktivitas', payload);
    toast.success("Aktivitas berhasil dibuat!");
    closeModal();
    await fetchAktivitas();

  } catch (error) {
    const errorMsg = error.response?.data?.detail?.[0]?.msg || "Gagal menyimpan. Periksa kembali isian Anda.";
    toast.error(errorMsg);
    console.error("Gagal menyimpan aktivitas:", error.response?.data || error.message);
  }
};

const openModal = () => { isModalOpen.value = true; };
const closeModal = () => { isModalOpen.value = false; };
</script>