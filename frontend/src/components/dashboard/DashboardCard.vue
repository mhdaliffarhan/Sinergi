<template>
  <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 flex items-center gap-4 transition-transform hover:scale-105 duration-300">
    <span class="text-3xl" :class="color">{{ icon }}</span>
    <div>
      <p class="text-lg font-bold text-gray-900 dark:text-white">{{ value }}</p>
      <p class="text-sm text-gray-500 dark:text-gray-400">{{ title }}</p>
    </div>
  </div>
</template>

<script setup>
import { defineProps } from 'vue';

const props = defineProps({
  icon: {
    type: String,
    required: true
  },
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  color: {
    type: String,
    default: 'text-gray-500'
  }
});
</script>