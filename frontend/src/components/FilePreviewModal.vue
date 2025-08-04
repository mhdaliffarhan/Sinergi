<template>
  <Transition name="modal-fade">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
      
      <div class="w-full h-full bg-white dark:bg-gray-800 flex flex-col">
        
        <div class="flex-shrink-0 flex items-center justify-between p-3 sm:p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-base sm:text-lg font-semibold text-gray-900 dark:text-white truncate pr-4" :title="fileName">
            {{ fileName || 'Preview Dokumen' }}
          </h3>
          <div class="flex items-center gap-2">
            <a :href="fileUrl" :download="fileName" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700">
              Unduh
            </a>
            <button @click="$emit('close')" class="p-2 rounded-full text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 dark:text-gray-400">
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
            </button>
          </div>
        </div>

        <div class="flex-grow bg-gray-200 dark:bg-gray-900 overflow-hidden">
          <iframe v-if="isPdf" :src="fileUrl" class="w-full h-full border-none" title="PDF Preview"></iframe>
          <img v-else-if="isImage" :src="fileUrl" class="w-full h-full object-contain" :alt="fileName">
          <div v-else class="flex items-center justify-center h-full">
            <div class="text-center p-4">
              <p class="text-lg font-semibold text-gray-700 dark:text-gray-300">Preview Tidak Tersedia</p>
              <p class="text-sm text-gray-500 dark:text-gray-400">Anda dapat mengunduh file untuk melihatnya.</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </Transition>
</template>

<script setup>
import { computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  show: { type: Boolean, default: false },
  fileUrl: { type: String, required: true },
  fileName: { type: String, required: true },
  fileType: { type: String, required: true }
});

const emit = defineEmits(['close']);

// Computed properties untuk menentukan tipe file
const isPdf = computed(() => props.fileType === 'application/pdf');
const isImage = computed(() => props.fileType.startsWith('image/'));

// Menutup modal saat tombol 'Escape' ditekan
const handleKeydown = (e) => {
  if (props.show && e.key === 'Escape') {
    emit('close');
  }
};

onMounted(() => {
  document.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown);
});
</script>

<style scoped>
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}
.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>