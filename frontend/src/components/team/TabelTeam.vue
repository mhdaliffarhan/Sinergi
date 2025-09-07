<template>
  <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="px-6 py-3 w-1/4">
            Nama Tim
          </th>
          <th scope="col" class="px-6 py-3 w-1/4">
            Ketua Tim
          </th>
          <th scope="col" class="px-6 py-3 w-1/4">
            Periode Aktif
          </th>
          <th scope="col" class="px-6 py-3 w-1/4">
            Jumlah Anggota
          </th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="team in teams" 
          :key="team.id" 
          @click="goToTeamDetail(team.id)"
          class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 cursor-pointer transition-colors"
        >
          <td scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            <div class="flex items-center">
              <div 
                class="flex-shrink-0 w-4 h-4 rounded-full mr-3"
                :style="{ backgroundColor: team.warna || '#3b82f6' }"
              ></div>
              <span class="font-medium">
                {{ team.namaTim }}
              </span>
            </div>
          </td>
          <td class="px-6 py-4">
            {{ team.ketuaTim?.namaLengkap || '-' }}
          </td>
          <td class="px-6 py-4">
            <div class="flex flex-col">
              <span class="flex items-center gap-2">
                <span>🗓️</span>
                <span>{{ formatDate(team.validFrom) }} - {{ formatDate(team.validUntil) }}</span>
              </span>
            </div>
          </td>
          <td class="px-6 py-4">
            {{ team.users?.length ?? 0 }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';
import { useRouter } from 'vue-router';
import { format } from 'date-fns';
import { id } from 'date-fns/locale';

const props = defineProps({
  teams: {
    type: Array,
    required: true,
  },
});

const router = useRouter();

const goToTeamDetail = (id) => {
  router.push({ name: 'team-detail', params: { id } });
};

const formatDate = (dateString) => {
  if (!dateString) return '-';
  const date = new Date(dateString);
  return format(date, 'd MMMM yyyy', { locale: id });
};
</script>