<template>
  <div v-if="dokumenWajibGrouped.length > 0" class="space-y-6">
    <div v-for="(group, index) in dokumenWajibGrouped" :key="index" class="bg-white dark:bg-gray-800 shadow-lg rounded-lg overflow-hidden">
      <div 
        @click="toggleGroup(group.aktivitasId)" 
        class="cursor-pointer p-4 sm:p-6 flex items-center justify-between transition-colors hover:bg-gray-50 dark:hover:bg-gray-700"
      >
        <div class="flex flex-col">
          <span class="text-sm font-medium text-blue-500 dark:text-blue-400">
            {{ group.aktivitas?.namaAktivitas || '-' }}
          </span>
          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
            {{ formatPeriode(group.aktivitas?.tanggalMulai, group.aktivitas?.tanggalSelesai) }}
          </p>
        </div>
        <div class="flex items-center gap-4">
          <span class="text-sm text-gray-500 dark:text-gray-400 hidden md:inline">
            {{ group.completedCount }} / {{ group.totalCount }} Dokumen Selesai
          </span>
          <svg :class="{'rotate-180': expandedGroups[group.aktivitasId]}" class="w-5 h-5 text-gray-500 transform transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path></svg>
        </div>
      </div>

      <div v-show="expandedGroups[group.aktivitasId]" class="p-4 sm:p-6 border-t border-gray-200 dark:border-gray-700">
        <ul class="divide-y divide-gray-200 dark:divide-gray-700">
          <li v-for="dokumen in group.dokumen" :key="dokumen.id" class="flex items-center justify-between py-2">
            <div class="flex-1 min-w-0">
              <span class="text-sm font-medium text-gray-900 dark:text-white">{{ dokumen.namaDokumen }}</span>
            </div>
            <div class="flex-shrink-0 flex items-center gap-2">
              <span :class="{'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300': dokumen.statusPengecekan, 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-300': !dokumen.statusPengecekan}"
                class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                {{ dokumen.statusPengecekan ? 'Selesai' : 'Belum' }}
              </span>
              <button @click="$emit('goToAktivitas', dokumen.aktivitas?.id)" class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-600 font-medium text-sm">
                Aksi
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
  <div v-else class="bg-white dark:bg-gray-800 shadow-md rounded-lg p-6 text-center text-gray-500 dark:text-gray-400">
    Tidak ada dokumen wajib yang terdaftar.
  </div>
</template>

<script setup>
import { ref, computed, watch, defineProps, defineEmits } from 'vue';
import { format } from 'date-fns';
import { id } from 'date-fns/locale';

const props = defineProps({
  dokumenWajib: {
    type: Array,
    required: true,
  },
});

const emits = defineEmits(['goToAktivitas']);
const expandedGroups = ref({});

const dokumenWajibGrouped = computed(() => {
  const groups = {};
  props.dokumenWajib.forEach(dokumen => {
    // Perbaikan: Tambahkan optional chaining untuk mencegah error
    if (!dokumen.aktivitas) return;
    const aktivitasId = dokumen.aktivitas.id;

    if (!groups[aktivitasId]) {
      groups[aktivitasId] = {
        aktivitasId,
        aktivitas: dokumen.aktivitas,
        dokumen: [],
        totalCount: 0,
        completedCount: 0,
      };
    }
    groups[aktivitasId].dokumen.push(dokumen);
    groups[aktivitasId].totalCount++;
    if (dokumen.statusPengecekan) {
      groups[aktivitasId].completedCount++;
    }
  });

  return Object.values(groups).sort((a, b) => new Date(b.aktivitas?.tanggalMulai) - new Date(a.aktivitas?.tanggalMulai));
});

const toggleGroup = (aktivitasId) => {
  expandedGroups.value[aktivitasId] = !expandedGroups.value[aktivitasId];
};

const formatPeriode = (start, end) => {
  const options = { day: 'numeric', month: 'short', year: 'numeric' };
  const startDate = start ? new Date(start) : null;
  const endDate = end ? new Date(end) : null;

  if (startDate && endDate) {
    return `${format(startDate, 'd MMMM yyyy', { locale: id })} - ${format(endDate, 'd MMMM yyyy', { locale: id })}`;
  }
  if (startDate) {
    return format(startDate, 'd MMMM yyyy', { locale: id });
  }
  return 'Tidak ada tanggal';
};

watch(dokumenWajibGrouped, () => {
  expandedGroups.value = {};
});
</script>