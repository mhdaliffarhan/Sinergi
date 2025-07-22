<template>
  <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="px-6 py-3">Nama Aktivitas</th>
          <th scope="col" class="px-6 py-3">Tim Penyelenggara</th>
          <th scope="col" class="px-6 py-3">Status Kelengkapan</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="activities.length === 0">
          <td colspan="3" class="px-6 py-4 text-center text-gray-500 dark:text-gray-400">
            🎉 Semua aktivitas sudah lengkap!
          </td>
        </tr>
        <tr v-for="item in activities" :key="item.id" @click="goToDetail(item.id)" class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 cursor-pointer">
          <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            {{ item.namaAktivitas }}
          </th>
          <td class="px-6 py-4">
            <span class="px-3 py-1 text-xs font-medium rounded-full bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300">
              {{ item.timPenyelenggara }}
            </span>
          </td>
          <td class="px-6 py-4">
            {{ getProgressText(item) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  activities: {
    type: Array,
    required: true,
  },
});

const router = useRouter();

const goToDetail = (id) => {
  router.push({ name: 'aktivitas-detail', params: { id: id } });
};

const getProgressText = (activity) => {
  const total = activity.daftarDokumenWajib.length;
  if (total === 0) return 'N/A';
  const completed = activity.daftarDokumenWajib.filter(doc => doc.status === 'Selesai').length;
  return `${completed} dari ${total} dokumen selesai`;
};
</script>