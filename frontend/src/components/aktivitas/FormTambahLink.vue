<template>
  <form @submit.prevent="handleSubmit">
    <div class="space-y-4">
      <div>
        <label for="url-link" class="block text-sm font-medium text-gray-700 dark:text-gray-300">URL / Tautan</label>
        <input 
          type="url" 
          id="url-link" 
          v-model="form.pathAtauUrl"
          class="mt-1 block w-full px-3 py-2 border text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          placeholder="https://contoh.com/dokumen-penting"
          required
        />
      </div>
      <div>
        <label for="keterangan-link" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Keterangan</label>
        <input 
          type="text" 
          id="keterangan-link" 
          v-model="form.keterangan"
          class="mt-1 block w-full px-3 py-2 border text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          placeholder="Contoh: Dokumen Paparan Rapat"
          required
        />
      </div>
    </div>
    <div class="mt-6 flex justify-end gap-3">
      <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700">Simpan Link</button>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue';
const emit = defineEmits(['close', 'submit']);
const form = reactive({ keterangan: '', pathAtauUrl: '' });
const handleSubmit = () => { emit('submit', form); };
</script>