<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-5 mb-4 border border-gray-200 dark:border-gray-700 cursor-pointer transition-transform transform hover:scale-[1.01]">
    <div class="flex items-center justify-between mb-2">
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
      
      <div v-if="team?.namaTim" class="flex items-center gap-2 mt-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-500" viewBox="0 0 20 20" fill="currentColor"><path d="M13 6a3 3 0 11-6 0 3 3 0 016 0zM18 8a2 2 0 11-4 0 2 2 0 014 0zM14 15a4 4 0 00-8 0v3h8v-3zM6 8a2 2 0 11-4 0 2 2 0 014 0zM16 18v-3a5.972 5.972 0 00-.75-2.906A3.005 3.005 0 0119 15v3h-3zM4.75 12.094A5.972 5.972 0 004 15v3H1v-3a3 3 0 013.75-2.906z" /></svg>
        <span>Tim: {{ team?.namaTim }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  id: { type: Number, required: true },
  namaProject: { type: String, required: true },
  team: { type: Object, default: () => ({}) },
  projectLeader: { type: Object, default: () => ({}) },
});
</script>