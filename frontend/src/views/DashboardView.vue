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
import { ref } from 'vue';
import DaftarAktivitas from '@/components/DaftarAktivitas.vue';
import ModalWrapper from '@/components/ModalWrapper.vue';
import FormBuatAktivitas from '@/components/FormBuatAktivitas.vue';

const aktivitas = ref([
  { id: 1, nama: 'Rapat Kick-off Proyek SUTAS 2025', tanggal: '15 Juli 2025', tim: 'Tim SUTAS', dokumen: 3 },
  { id: 2, nama: 'Pelatihan Penggunaan Aplikasi SINERGI', tanggal: '16 Juli 2025', tim: 'Divisi IT', dokumen: 1 },
]);

const isModalOpen = ref(false);
const openModal = () => { isModalOpen.value = true; };
const closeModal = () => { isModalOpen.value = false; };

const handleActivitySubmit = (formData) => {
  // 1. Buat variabel untuk menampung string tanggal yang akan ditampilkan
  let tanggalTampil = '';

  // Opsi untuk memformat tanggal agar lebih mudah dibaca (e.g., "15 Juli 2025")
  const formatDate = (dateString) => {
    if (!dateString) return '';
    return new Date(dateString).toLocaleDateString('id-ID', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  };
  
  // 2. Cek apakah 'Gunakan rentang tanggal' dicentang
  if (formData.useDateRange) {
    tanggalTampil = `${formatDate(formData.tanggalMulai)} - ${formatDate(formData.tanggalSelesai)}`;
  } else {
    tanggalTampil = formatDate(formData.tanggal);
  }

  // 3. Cek apakah 'Gunakan jam' dicentang, lalu tambahkan ke string
  if (formData.useTime) {
    tanggalTampil += ` | ${formData.jamMulai} - ${formData.jamSelesai} WITA`;
  }
  
  // 4. Buat objek aktivitas baru dengan data yang sudah diformat
  const newActivity = {
    id: Date.now(),
    nama: formData.nama,
    tanggal: tanggalTampil, // Gunakan string yang sudah diformat
    tim: formData.tim,
    dokumen: 0,
  };
  
  aktivitas.value.unshift(newActivity);
};
</script>