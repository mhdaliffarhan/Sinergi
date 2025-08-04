<template>
  <div>
    <div v-if="!item.dokumenTerkait" class="flex items-center justify-between p-3">
      <span class="text-sm font-medium text-gray-800 dark:text-gray-200">{{ item.namaDokumen }}</span>
      <div class="flex items-center gap-2">
        <span class="text-xs font-medium px-2.5 py-1 rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300">
          Wajib Diunggah
        </span>
        <button @click="$emit('unggah', item.id)" class="px-3 py-1 text-xs font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700">
          Unggah
        </button>
      </div>
    </div>

    <div v-else>
      <DokumenItem 
        :dokumen="item.dokumenTerkait"
        @hapus="$emit('hapus', item.dokumenTerkait.id)"
      />
    </div>
  </div>
</template>

<script setup>
import DokumenItem from '@/components/aktivitas/DokumenItem.vue';

defineProps({
  item: {
    type: Object,
    required: true,
  }
});

defineEmits(['unggah', 'hapus']);
</script>