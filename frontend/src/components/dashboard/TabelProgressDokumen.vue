<template>
  <div class="overflow-x-auto rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="px-6 py-3">Aktivitas</th>
          <th scope="col" class="px-6 py-3">Dokumen Wajib</th>
          <th scope="col" class="px-6 py-3 text-center">Status</th>
          <th scope="col" class="px-6 py-3 text-center">Tindakan</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="dokumenWajib.length === 0">
          <td colspan="4" class="px-6 py-4 text-center text-gray-500 dark:text-gray-400">
            Tidak ada dokumen wajib yang harus diselesaikan.
          </td>
        </tr>
        <tr v-for="dokumen in dokumenWajib" :key="dokumen.id" class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
          <td class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            <span class="inline-flex items-center w-fit px-2 py-1 text-xs font-medium rounded-full text-white mr-2"
                  :style="{ backgroundColor: dokumen.team?.warna || '#3b82f6' }">
              {{ dokumen.team?.namaTim || '-' }}
            </span>
            <span>{{ dokumen.aktivitas?.namaAktivitas || '-' }}</span>
          </td>
          <td class="px-6 py-4">{{ dokumen.namaDokumen }}</td>
          <td class="px-6 py-4 text-center">
            <span :class="{'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-300': dokumen.statusPengecekan, 'bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-300': !dokumen.statusPengecekan}"
                  class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
              {{ dokumen.statusPengecekan ? 'Selesai' : 'Belum' }}
            </span>
          </td>
          <td class="px-6 py-4 text-center">
            <button @click="$emit('goToAktivitas', dokumen.aktivitas.id)" class="text-blue-600 hover:text-blue-900 dark:text-blue-400 dark:hover:text-blue-600 font-medium">
              Detail
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  dokumenWajib: {
    type: Array,
    required: true
  }
});

const emits = defineEmits(['goToAktivitas']);
</script>