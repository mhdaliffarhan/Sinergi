<template>
  <router-link 
    :to="{ name: 'project-detail', params: { id: id } }"  
    class="block p-4 mb-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-200"
  >  <div class="flex items-center justify-between mb-2">
      <h3 class="text-xl font-semibold text-gray-800 dark:text-gray-100">{{ namaProject }}</h3>
      <span class="inline-flex items-center px-2 py-1 text-xs font-medium rounded-full text-white"
        :style="{ backgroundColor: team?.warna || '#3b82f6' }">
        {{ team?.namaTim || '-' }}
      </span>
    </div>
    
    <div class="text-sm text-gray-500 dark:text-gray-400">
      <div class="flex items-center gap-2 mt-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-green-500" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" /></svg>
        <span>Project Leader: {{ projectLeader?.namaLengkap || '-' }}</span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  id: { type: Number, required: true },
  namaProject: { type: String, required: true },
  team: { type: Object, default: () => ({}) },
  projectLeader: { type: Object, default: () => ({}) },
});
</script>