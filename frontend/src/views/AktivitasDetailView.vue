<template>
  <div>
     <Breadcrumbs :items="breadcrumbItems" />

    <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
      <div v-if="aktivitas">
        <p class="text-sm text-blue-500 font-semibold">{{ aktivitas.timPenyelenggara }}</p>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mt-1">{{ aktivitas.namaAktivitas }}</h1>
        <p class="mt-2 text-base text-gray-500 dark:text-gray-400">{{ aktivitas.formattedTanggal }}</p>

        <hr class="my-6 border-gray-200 dark:border-gray-700">

        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-2">Deskripsi</h2>
        <p class="text-gray-600 dark:text-gray-300 whitespace-pre-wrap">{{ aktivitas.deskripsi }}</p>

        <hr class="my-6 border-gray-200 dark:border-gray-700">

        <h2 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">Dokumen Terlampir</h2>
        <div class="p-4 text-center border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg">
          <p class="text-sm text-gray-500 dark:text-gray-400">Belum ada dokumen yang diunggah.</p>
        </div>
      </div>
      <div v-else>
        <p>Memuat data aktivitas...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Breadcrumbs from '@/components/Breadcrumbs.vue';

const route = useRoute();
const aktivitasId = route.params.id;

const breadcrumbItems = ref([
  { text: 'Dashboard', to: '/dashboard' },
  { text: 'Detail Aktivitas' } // Item terakhir tidak perlu properti 'to'
]);

// Untuk sementara, kita gunakan data palsu.
// Di langkah berikutnya, kita akan mengambil data ini dari API.
const aktivitas = ref(null);

const fetchDetailAktivitas = async () => {
  console.log(`Mengambil data untuk aktivitas dengan ID: ${aktivitasId}`);
  // Logika untuk memanggil API akan ditambahkan di sini.
  // Contoh data palsu:
  aktivitas.value = {
    id: aktivitasId,
    namaAktivitas: 'Rapat Kick-off Proyek SUTAS 2025',
    timPenyelenggara: 'Tim SUTAS',
    formattedTanggal: '15 Juli 2025',
    deskripsi: 'Rapat awal untuk membahas timeline dan pembagian tugas Proyek Sensus Pertanian Lanjutan (SUTAS) tahun 2025.'
  };
};

onMounted(() => {
  fetchDetailAktivitas();
});
</script>