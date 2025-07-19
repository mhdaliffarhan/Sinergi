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

      <button v-if="item.status !== 'Selesai'" @click="$emit('upload', item.id)" class="px-3 py-1 text-xs font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700">
        Upload
      </button>
      <button v-else class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded-md cursor-not-allowed">
        Selesai
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

defineEmits(['upload']);
</script>