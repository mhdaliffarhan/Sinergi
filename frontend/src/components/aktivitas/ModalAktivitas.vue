<template>
  <ModalWrapper :show="showModal" @close="handleCloseModal" :title="aktivitas?.namaAktivitas || 'Detail Aktivitas'">
    <div v-if="aktivitas" class="space-y-4">
      <div>
        <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Tim Terkait</p>
        <div class="flex items-center gap-2 mt-1">
          <div class="w-4 h-4 rounded-full" :style="{ backgroundColor: aktivitas.team?.warna || '#3b82f6' }"></div>
          <span class="text-base font-semibold text-gray-900 dark:text-white">{{ aktivitas.team?.namaTim || '-' }}</span>
        </div>
      </div>
      <div>
        <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Jadwal</p>
        <p class="mt-1 text-base text-gray-900 dark:text-white">{{ formatJadwal(aktivitas) }}</p>
      </div>
      <div v-if="aktivitas.deskripsi">
        <p class="text-sm font-medium text-gray-500 dark:text-gray-400">Deskripsi</p>
        <p class="mt-1 text-base text-gray-900 dark:text-white">{{ aktivitas.deskripsi }}</p>
      </div>
      <div class="mt-6 flex justify-end gap-2 border-t border-gray-200 dark:border-gray-700 pt-4">
        <button @click="handleCloseModal" class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-600">
          Tutup
        </button>
        <button @click="goToDetail" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 transition-colors">
          Lihat Detail
        </button>
      </div>
    </div>
    <div v-else class="text-center text-gray-500 dark:text-gray-400">
      Gagal memuat data aktivitas.
    </div>
  </ModalWrapper>
</template>

<script setup>
import { defineProps, defineEmits, computed } from 'vue';
import { format, isSameDay } from 'date-fns';
import { id } from 'date-fns/locale';
import ModalWrapper from '@/components/ModalWrapper.vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  aktivitas: {
    type: Object,
    required: true
  }
});

const emits = defineEmits(['close', 'goToDetail']); // Memancarkan event 'goToDetail'

const router = useRouter();

// Gunakan computed property untuk mengelola tampilan modal
const showModal = computed(() => !!props.aktivitas);

const formatJadwal = (aktivitas) => {
  if (!aktivitas.tanggalMulai) return '-';

  const tglMulai = new Date(aktivitas.tanggalMulai);
  const tglSelesai = aktivitas.tanggalSelesai ? new Date(aktivitas.tanggalSelesai) : null;
  
  const formattedTgl = (tgl) => format(tgl, 'd MMMM yyyy', { locale: id });
  
  let tanggalTampil = '';
  if (tglSelesai && !isSameDay(tglMulai, tglSelesai)) {
    tanggalTampil = `${formattedTgl(tglMulai)} - ${formattedTgl(tglSelesai)}`;
  } else {
    tanggalTampil = formattedTgl(tglMulai);
  }

  let waktuTampil = '';
  if (aktivitas.jamMulai && aktivitas.jamSelesai) {
    waktuTampil = `Pukul ${aktivitas.jamMulai.substring(0, 5)} - ${aktivitas.jamSelesai.substring(0, 5)} WITA`;
  } else if (aktivitas.jamMulai) {
    waktuTampil = `Pukul ${aktivitas.jamMulai.substring(0, 5)} WITA`;
  }

  return `${tanggalTampil} ${waktuTampil}`.trim();
};

const handleCloseModal = () => {
  emits('close');
};

const goToDetail = () => {
  emits('close');
  // Emits the event to the parent so the parent can handle the navigation
  emits('goToDetail', props.aktivitas.id); 
};
</script>