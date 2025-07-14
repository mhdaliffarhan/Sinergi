<template>
  <div>
    <KartuAktivitas
      v-for="item in aktivitas"
      :key="item.id"
      :nama_aktivitas="item.nama"
      :tanggal="item.tanggal"
      :nama_tim="item.tim"
      :jumlah_dokumen="item.dokumen"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import KartuAktivitas from '@/components/KartuAktivitas.vue';

// Untuk saat ini, kita gunakan data palsu (mock data).
// Nanti, data ini akan diambil dari API backend.
const aktivitas = ref([
  { id: 1, nama: 'Rapat Kick-off Proyek SUTAS 2025', tanggal: '15 Juli 2025', tim: 'Tim SUTAS', dokumen: 3 },
  { id: 2, nama: 'Pelatihan Penggunaan Aplikasi SINERGI', tanggal: '16 Juli 2025', tim: 'Divisi IT', dokumen: 1 },
  { id: 3, nama: 'Rapat Evaluasi Bulanan Neraca', tanggal: '17 Juli 2025', tim: 'Tim Neraca', dokumen: 5 },
  { id: 4, nama: 'Survei Harga Konsumen Minggu ke-3', tanggal: '18 Juli 2025', tim: 'Tim Statistik Harga', dokumen: 8 },
]);
</script>