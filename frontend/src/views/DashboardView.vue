<template>
  <div class="p-6">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-green-700 dark:text-green-500">Dashboard Aktivitas</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Selamat datang kembali! Ini adalah daftar aktivitas terbaru.</p>
      </div>
      <div class="mt-4 sm:mt-0">
        <button @click="openModal" class="w-full sm:w-auto flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 transition-colors">
          <span>+</span>
          <span>Buat Aktivitas Baru</span>
        </button>
      </div>
    </div>

    <DaftarAktivitas :aktivitas="aktivitas" />

    <ModalWrapper :show="isModalOpen" @close="closeModal" title="Buat Aktivitas Baru">
      <FormBuatAktivitas @close="closeModal" @submit="handleActivitySubmit" />
    </ModalWrapper>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import DaftarAktivitas from '@/components/DaftarAktivitas.vue';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormBuatAktivitas from '@/components/FormBuatAktivitas.vue';

const aktivitas = ref([]);
const isModalOpen = ref(false);

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
    
    closeModal();
    await fetchAktivitas();

  } catch (error) {
    console.error("Gagal menyimpan aktivitas:", error.response?.data || error.message);
  }
};

const openModal = () => { isModalOpen.value = true; };
const closeModal = () => { isModalOpen.value = false; };
</script>