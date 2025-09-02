<template>
  <router-link :to="`/aktivitas/detail/${aktivitas.id}`" class="block w-full h-full">
    <div class="flex flex-col h-full p-4 bg-white dark:bg-gray-700 rounded-lg shadow-sm border border-gray-200 dark:border-gray-600 transition-transform transform hover:scale-[1.01] hover:shadow-md">
      
      <div class="flex items-start gap-3 flex-grow">
        <div class="flex-shrink-0 p-1.5 rounded-full bg-blue-50 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400">
          <svg class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M15 14h.01" /></svg>
        </div>
        <div class="flex-grow">
          <h3 class="text-sm font-semibold text-gray-900 dark:text-white leading-tight">
            {{ aktivitas.namaAktivitas }}
          </h3>
        </div>
      </div>
      
      <div class="mt-4 flex flex-col gap-3">
        <div v-if="totalDokumenWajib > 0" class="flex items-center gap-6">
          <div class="flex-1 flex flex-col items-center">
            <div class="relative h-16 w-16">
              <svg class="h-full w-full" viewBox="0 0 36 36">
                <path class="stroke-gray-200 dark:stroke-gray-600" d="M18 2.0845a15.9155 15.9155 0 010 31.831a15.9155 15.9155 0 010-31.831" fill="none" stroke-width="2.5" stroke-dasharray="100, 100" />
                <path class="stroke-green-500" :d="`M18 2.0845a15.9155 15.9155 0 010 31.831a15.9155 15.9155 0 010-31.831`" fill="none" stroke-width="2.5" stroke-dasharray="100, 100" :style="{ 'stroke-dashoffset': pengumpulanOffset }" />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-sm font-bold text-gray-900 dark:text-white">
                  {{ dokumenTerkumpul }}/{{ totalDokumenWajib }}
                </span>
              </div>
            </div>
            <p class="mt-1 text-xs text-gray-500 dark:text-gray-400 text-center">Pengumpulan</p>
          </div>

          <div class="flex-1 flex flex-col items-center">
            <div class="relative h-16 w-16">
              <svg class="h-full w-full" viewBox="0 0 36 36">
                <path class="stroke-gray-200 dark:stroke-gray-600" d="M18 2.0845a15.9155 15.9155 0 010 31.831a15.9155 15.9155 0 010-31.831" fill="none" stroke-width="2.5" stroke-dasharray="100, 100" />
                <path class="stroke-blue-500" :d="`M18 2.0845a15.9155 15.9155 0 010 31.831a15.9155 15.9155 0 010-31.831`" fill="none" stroke-width="2.5" stroke-dasharray="100, 100" :style="{ 'stroke-dashoffset': pemeriksaanOffset }" />
              </svg>
              <div class="absolute inset-0 flex items-center justify-center">
                <span class="text-sm font-bold text-gray-900 dark:text-white">
                  {{ dokumenTerverifikasi }}/{{ totalDokumenWajib }}
                </span>
              </div>
            </div>
            <p class="mt-1 text-xs text-gray-500 dark:text-gray-400 text-center">Pemeriksaan</p>
          </div>
        </div>
        
        <div v-else class="text-center p-4">
          <p class="text-sm text-gray-500 dark:text-gray-400">Tidak ada dokumen wajib.</p>
        </div>
      </div>
      
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  aktivitas: {
    type: Object,
    required: true,
  },
});

const totalDokumenWajib = computed(() => {
  return props.aktivitas.daftarDokumenWajib?.length || 0;
});

const dokumenTerkumpul = computed(() => {
  if (totalDokumenWajib.value === 0) return 0;
  return props.aktivitas.daftarDokumenWajib.filter(doc => doc.dokumenId !== null).length;
});

const dokumenTerverifikasi = computed(() => {
  if (totalDokumenWajib.value === 0) return 0;
  return props.aktivitas.daftarDokumenWajib.filter(doc => doc.statusPengecekan === true).length;
});

const pengumpulanOffset = computed(() => {
  if (totalDokumenWajib.value === 0) return 0;
  const progress = (dokumenTerkumpul.value / totalDokumenWajib.value) * 100;
  return 100 - progress;
});

const pemeriksaanOffset = computed(() => {
  if (totalDokumenWajib.value === 0) return 0;
  const progress = (dokumenTerverifikasi.value / totalDokumenWajib.value) * 100;
  return 100 - progress;
});
</script>