<template>
  <router-link 
    to="/detail/1" 
    class="block p-4 mb-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-200"
  >
    <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-2">
      {{ nama_aktivitas }}
    </h3>

    <div class="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400 mb-3">
      <div class="flex items-center gap-1">
        <span>📅</span>
        <span>{{ tanggal }}</span>
      </div>
      <div class="flex items-center gap-1">
        <span>👥</span>
        <span>{{ nama_tim }}</span>
      </div>
    </div>

    <div class="text-right">
      <p class="text-sm font-medium text-gray-700 dark:text-gray-300">
        {{ jumlah_dokumen }} Dokumen
      </p>
    </div>
  </router-link>
</template>

<script setup>
defineProps({
  nama_aktivitas: { type: String, required: true },
  tanggal: { type: String, required: true },
  nama_tim: { type: String, required: true },
  jumlah_dokumen: { type: Number, default: 0 },
});
</script>