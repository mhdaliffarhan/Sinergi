<template>
  <div>
    <Breadcrumbs :items="breadcrumbItems" />
    <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <div v-if="isLoading">
        <p class="text-center text-gray-500 dark:text-gray-400">Memuat data aktivitas...</p>
      </div>
      <div v-else-if="aktivitas">
        <div class="flex items-start justify-between">
            <div>
              <p class="text-sm text-blue-500 font-semibold">{{ aktivitas.timPenyelenggara }}</p>
              <h1 class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ aktivitas.namaAktivitas }}</h1>
              
              <p class="mt-2 text-base text-gray-500 dark:text-gray-400 max-w-3xl">{{ aktivitas.deskripsi }}</p>
            </div>
            <button @click="openEditModal" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 ml-4 flex-shrink-0">
              Edit
            </button>
          </div>
        <ModalWrapper :show="isEditModalOpen" @close="closeEditModal" title="Edit Aktivitas">
          <FormBuatAktivitas :initial-data="aktivitas" @close="closeEditModal" @submit="handleUpdateActivity" />
        </ModalWrapper>

        <div class="mt-4 flex flex-wrap items-center gap-3 border-t border-gray-200 dark:border-gray-700 pt-4">
          <div class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-100 dark:bg-gray-700">
            <span class="text-lg">🗓️</span>
            <span class="text-sm font-medium text-gray-700 dark:text-gray-200">{{ formattedWaktuPelaksanaan.tanggal }}</span>
          </div>
          
          <div v-if="aktivitas.jamMulai" class="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-100 dark:bg-gray-700">
            <span class="text-lg">🕒</span>
            <span class="text-sm font-medium text-gray-700 dark:text-gray-200">{{ formattedWaktuPelaksanaan.waktu }}</span>
          </div>
        </div>

        <hr class="my-6 border-gray-200 dark:border-gray-700">

        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">Dokumen Terlampir</h2>
        <div class="p-4 text-center border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
          <p class="text-sm text-gray-500 dark:text-gray-400">Belum ada dokumen yang diunggah.</p>
        </div>
      </div>
      <div v-else>
        <p class="text-center text-red-500">Gagal memuat data atau aktivitas tidak ditemukan.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
import { useToast } from 'vue-toastification';
import Breadcrumbs from '@/components/Breadcrumbs.vue';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormBuatAktivitas from '@/components/FormBuatAktivitas.vue';

const route = useRoute();
const toast = useToast();
const aktivitasId = route.params.id;

const aktivitas = ref(null);
const isLoading = ref(true);
const breadcrumbItems = ref([
  { text: 'Dashboard', to: '/dashboard' },
  { text: 'Detail Aktivitas' }
]);

// --- LOGIKA BARU UNTUK MODAL EDIT ---
const isEditModalOpen = ref(false);

const openEditModal = () => { isEditModalOpen.value = true;};
const closeEditModal = () => {isEditModalOpen.value = false;};

// Fungsi konversi
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

const formattedWaktuPelaksanaan = computed(() => {
  if (!aktivitas.value) return { tanggal: '', waktu: '' };

  const options = { day: 'numeric', month: 'long', year: 'numeric' };
  let tanggalTampil = '';
  let waktuTampil = '';

  const tglMulai = new Date(aktivitas.value.tanggalMulai);
  
  if (aktivitas.value.tanggalSelesai) {
    const tglSelesai = new Date(aktivitas.value.tanggalSelesai);
    // Format rentang
    const mulai = tglMulai.toLocaleDateString('id-ID', { day: 'numeric', month: 'long' });
    const selesai = tglSelesai.toLocaleDateString('id-ID', options);
    tanggalTampil = `${mulai} - ${selesai}`;
  } else {
    // Format tanggal tunggal
    tanggalTampil = tglMulai.toLocaleDateString('id-ID', options);
  }

  if (aktivitas.value.jamMulai) {
    waktuTampil = `${aktivitas.value.jamMulai} - ${aktivitas.value.jamSelesai} WITA`;
  }

  return { tanggal: tanggalTampil, waktu: waktuTampil };
});

const fetchDetailAktivitas = async () => {
  isLoading.value = true;
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/aktivitas/${aktivitasId}`);
    aktivitas.value = convertKeysToCamelCase(response.data);
    console.log(aktivitas.value);
    // Perbarui judul di breadcrumbs dengan nama aktivitas asli
    breadcrumbItems.value[1].text = aktivitas.value.namaAktivitas;

  } catch (error) {
    toast.error("Gagal memuat detail aktivitas atau aktivitas tidak ditemukan.");
    console.error(error);
  } finally {
    isLoading.value = false;
  }
};

const handleUpdateActivity = async (formData) => {
  const payload = { ...formData };
  // Logika pembersihan data null tetap ada
  const nullableFields = ['tanggalMulai', 'tanggalSelesai', 'jamMulai', 'jamSelesai'];
  nullableFields.forEach(field => {
    if (payload[field] === '') payload[field] = null;
  });
  console.log('data : ', payload.data);
  try {
    // Kirim data ke endpoint PUT dengan ID yang sesuai
    await axios.put(`http://127.0.0.1:8000/api/aktivitas/${aktivitasId}`, payload);
    
    toast.success("Aktivitas berhasil diperbarui!");
    closeEditModal();
    await fetchDetailAktivitas(); // Ambil ulang data untuk menampilkan perubahan
  } catch (error) {
    const errorMsg = error.response?.data?.detail || "Gagal memperbarui aktivitas.";
    toast.error(errorMsg);
    console.error(error);
  }
};

onMounted(() => {
  fetchDetailAktivitas();
});
</script>