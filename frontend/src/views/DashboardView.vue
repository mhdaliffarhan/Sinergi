<template>
  <div class="p-6">
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Dashboard Aktivitas</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Selamat datang kembali! Ini adalah daftar aktivitas terbaru.</p>
      </div>
      <div class="mt-4 sm:mt-0">
        <button @click="openModal" class="w-full sm:w-auto flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg shadow-md hover:bg-blue-700 transition-colors">
          <span>+</span>
          <span>Buat Aktivitas Baru</span>
        </button>
      </div>
    </div>

    <DaftarAktivitas />

    <ModalWrapper :show="isModalOpen" @close="closeModal" title="Buat Aktivitas Baru">
      <FormBuatAktivitas @close="closeModal" @submit="handleActivitySubmit" />
    </ModalWrapper>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import DaftarAktivitas from '@/components/DaftarAktivitas.vue';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormBuatAktivitas from '@/components/FormBuatAktivitas.vue';

// 1. State untuk mengontrol visibilitas modal
const isModalOpen = ref(false);

// 2. Fungsi untuk membuka dan menutup modal
const openModal = () => {
  isModalOpen.value = true;
};
const closeModal = () => {
  isModalOpen.value = false;
};

// 3. Fungsi untuk menangani data saat form di-submit
const handleActivitySubmit = (formData) => {
  console.log('Aktivitas baru berhasil dibuat:', formData);
  // Di sini nanti Anda bisa menambahkan logika untuk mengirim data ke backend
  // dan memperbarui daftar aktivitas di halaman.
};
</script>