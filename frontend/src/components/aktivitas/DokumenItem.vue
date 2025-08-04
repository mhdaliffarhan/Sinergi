<template>
  <div class="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors">
    <div class="flex items-center gap-4 overflow-hidden">
      <span class="text-2xl flex-shrink-0">{{ dokumen.tipe === 'FILE' ? '📄' : '🔗' }}</span>
      <div class="overflow-hidden">
        <p class="font-semibold text-gray-800 dark:text-gray-100 truncate">{{ dokumen.keterangan }}</p>
        <p v-if="dokumen.namaFileAsli" class="text-xs text-gray-500 dark:text-gray-400 truncate">{{ dokumen.namaFileAsli }}</p>
      </div>
    </div>
    <div class="flex items-center gap-2 flex-shrink-0 ml-2">
      <a v-if="dokumen.tipe === 'LINK'" :href="dokumen.pathAtauUrl" target="_blank" class="px-3 py-1.5 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700">
        Buka Link
      </a>
      <button v-else @click="$emit('preview', dokumen)" class="px-3 py-1.5 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700">
        Lihat File
      </button>
      <button @click="$emit('hapus', dokumen.id)" class="p-2 rounded-full text-gray-500 hover:bg-red-100 hover:text-red-600 dark:hover:bg-red-900/50">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  dokumen: {
    type: Object,
    required: true
  }
});

// Daftarkan event 'hapus' dan 'preview'
defineEmits(['hapus', 'preview']);
</script>