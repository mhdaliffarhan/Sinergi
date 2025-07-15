<template>
  <div 
    @click="openFilePicker"
    @dragover.prevent="handleDragOver"
    @dragleave.prevent="handleDragLeave"
    @drop.prevent="handleDrop"
    :class="{ 'border-blue-500 bg-blue-50 dark:bg-gray-700': isDragging }"
    class="mt-4 border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center cursor-pointer transition-colors duration-200"
  >
    <input type="file" ref="fileInput" @change="handleFileSelect" class="hidden">
    
    <div class="flex flex-col items-center">
      <svg class="w-12 h-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-4-4V7a4 4 0 014-4h.586a1 1 0 01.707.293l4.414 4.414a1 1 0 01.293.707V16m-4-8h4m-4 8L7 8m1 9l-5-5m10 5l5-5" /></svg>
      <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
        <span class="font-semibold text-blue-600 dark:text-blue-400">Klik untuk memilih</span> atau seret & lepas file di sini
      </p>
      <p class="text-xs text-gray-500 dark:text-gray-500">Mendukung semua jenis file</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['file-selected']);
const fileInput = ref(null);
const isDragging = ref(false);

const openFilePicker = () => {
  fileInput.value.click();
};

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    emit('file-selected', file);
  }
};

const handleDragOver = () => { isDragging.value = true; };
const handleDragLeave = () => { isDragging.value = false; };
const handleDrop = (event) => {
  isDragging.value = false;
  const file = event.dataTransfer.files[0];
  if (file) {
    emit('file-selected', file);
  }
};
</script>