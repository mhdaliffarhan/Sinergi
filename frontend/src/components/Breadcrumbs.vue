<template>
  <nav aria-label="Breadcrumb" class="mb-4 pt-2">
    <ol class="flex items-center gap-1.5 text-sm text-gray-600 dark:text-gray-400">
      <li v-for="(item, index) in items" :key="index" class="flex items-center">

        <router-link 
          v-if="item.to" 
          :to="item.to" 
          class="hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
        >
          {{ item.text }}
        </router-link>

        <span v-else class="font-medium text-green-400 dark:text-green-500">
          {{ item.text }}
        </span>

        <span v-if="index < items.length - 1" class="mx-1.5">
          /
        </span>
      </li>
    </ol>
  </nav>
</template>

<script setup>
defineProps({
  items: {
    type: Array,
    required: true,
    default: () => []
  }
});
</script>