<template>
  <div>
    <p class="text-sm text-gray-600 dark:text-gray-300">
      Anda akan mengganti file yang sudah ada. Apa yang ingin Anda lakukan dengan file yang lama?
    </p>

    <div class="mt-6 flex flex-col sm:flex-row gap-3">
      <button 
        @click="$emit('pilih', 'hapus')"
        class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-red-600 text-base font-medium text-white hover:bg-red-700 focus:outline-none"
      >
        Hapus Permanen File Lama
      </button>

      <button 
        @click="$emit('pilih', 'unlink')"
        class="w-full inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-500 shadow-sm px-4 py-2 bg-white dark:bg-gray-700 text-base font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none"
      >
        Lepaskan Tautan Saja (Unlink)
      </button>
    </div>
  </div>
</template>

<script setup>
defineEmits(['pilih']);
</script>