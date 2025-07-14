<template>
  <div class="bg-gray-50 min-h-screen">
    <main class="max-w-3xl mx-auto p-4 sm:p-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">Dashboard Aktivitas</h1>

      <KartuAktivitas
        nama_aktivitas="Rapat Kick-off Proyek SUTAS 2025"
        tanggal="14 Juli 2025"
        nama_tim="Tim SUTAS"
        :jumlah_dokumen="3"
      />

      <KartuAktivitas
        nama_aktivitas="Pelatihan Penggunaan Aplikasi SINERGI"
        tanggal="15 Juli 2025"
        nama_tim="Divisi IT"
        :jumlah_dokumen="1"
      />

      <KartuAktivitas
        nama_aktivitas="Rapat Evaluasi Bulanan"
        tanggal="16 Juli 2025"
        nama_tim="Tim Neraca"
      />
    </main>
  </div>
</template>

<script setup>
import KartuAktivitas from '@/components/KartuAktivitas.vue';
</script>