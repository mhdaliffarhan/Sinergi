<template>
  <div class="p-6">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Dashboard Aktivitas</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Selamat datang kembali! Ini adalah daftar aktivitas terbaru.</p>
      </div>
      <div class="mt-4 sm:mt-0">
        <button class="w-full sm:w-auto flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 transition-colors">
          <span>+</span>
          <span>Buat Aktivitas Baru</span>
        </button>
      </div>
    </div>

    <DaftarAktivitas />
  </div>
</template>

<script setup>
import DaftarAktivitas from '@/components/DaftarAktivitas.vue';
</script>