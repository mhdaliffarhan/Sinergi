<template>
  <div class="flex items-center justify-between p-3">
    <span class="text-sm font-medium text-gray-800 dark:text-gray-200">{{ item.namaDokumen }}</span>
    
    <div class="flex items-center gap-2">
      <span 
        :class="item.status === 'Selesai' ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300' : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300'"
        class="text-xs font-medium px-2.5 py-1 rounded-full"
      >
        {{ item.status }}
      </span>

      <button 
        v-if="item.status !== 'Selesai'" 
        @click="$emit('unggah', item.id)" 
        class="px-3 py-1 text-xs font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700"
      >
        Unggah
      </button>
      
      <button 
        v-else 
        @click="$emit('ganti', item)" 
        class="px-3 py-1 text-xs font-medium text-gray-700 dark:text-gray-200 bg-gray-200 dark:bg-gray-600 rounded-md hover:bg-gray-300 dark:hover:bg-gray-500"
      >
        Ganti File
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  item: {
    type: Object,
    required: true,
  }
});

defineEmits(['unggah', 'ganti']);
</script>