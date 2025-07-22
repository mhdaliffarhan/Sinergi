<template>
  <Transition name="modal-fade">
    <div v-if="show" class="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div 
        @click="$emit('close')" 
        class="absolute inset-0 bg-black/60"
      ></div>
  
      <div class="relative w-full max-w-lg bg-white dark:bg-gray-800 rounded-xl shadow-xl flex flex-col max-h-[90vh]">
        <div class="flex-shrink-0 flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            {{ title }}
          </h3>
          <button 
            @click="$emit('close')" 
            class="p-2 rounded-full text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-700 dark:text-gray-400"
          >
            <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
  
        <div class="flex-grow p-6 overflow-y-auto">
          <slot />
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue';

// Komponen ini menerima properti dari parent
defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  title: {
    type: String,
    default: 'Judul Modal',
  },
});

// Komponen ini akan 'memancarkan' event 'close' ke parent
const emit = defineEmits(['close']);

// Menutup modal saat tombol 'Escape' ditekan
const handleKeydown = (e) => {
  if (e.key === 'Escape') {
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
  transition: all 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>