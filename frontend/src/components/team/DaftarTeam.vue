<template>
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div
      v-for="team in teams"
      :key="team.id"
      class="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden transition-transform transform hover:scale-105 cursor-pointer"
      @click="goToTeamDetail(team.id)"
    >
      <div class="p-6">
        <div class="flex items-center justify-between">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">
            {{ team.namaTim }}
          </h3>
          <div
            class="w-4 h-4 rounded-full"
            :style="{ backgroundColor: team.warna || '#3b82f6' }"
          ></div>
        </div>
        <p class="mt-2 text-sm text-gray-500 dark:text-gray-400">
          Tim ini aktif dari {{ formatDate(team.validFrom) }} hingga
          {{ formatDate(team.validUntil) }}.
        </p>
        <div class="mt-4 flex items-center text-sm text-gray-500 dark:text-gray-400">
          <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
            <path
              fill-rule="evenodd"
              d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z"
              clip-rule="evenodd"
            ></path>
          </svg>
          <span class="ml-1">{{ team.users.length }} Anggota</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
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
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return format(date, 'd MMMM yyyy', { locale: id });
};
</script>