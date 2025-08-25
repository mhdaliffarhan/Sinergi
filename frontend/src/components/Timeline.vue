<template>
  <div class="max-w-3xl mx-auto">
    <h2 class="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">Timeline Aktivitas</h2>
    <ol class="relative border-l border-gray-300 dark:border-gray-600">
      <li v-for="item in events" :key="item.id" class="mb-10 ml-6 cursor-pointer group"
          @click="$router.push(`/aktivitas/detail/${item.id}`)">
        <span class="absolute flex items-center justify-center w-6 h-6 bg-blue-500 rounded-full -left-3 ring-8 ring-white dark:ring-gray-900">
          <svg class="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd"
              d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-11a1 1 0 10-2 0v3a1 1 0 002 0V7zm0 6a1 1 0 11-2 0 1 1 0 012 0z"
              clip-rule="evenodd" />
          </svg>
        </span>
        <div class="p-4 bg-white border border-gray-200 rounded-lg shadow-sm group-hover:shadow-md dark:bg-gray-800 dark:border-gray-700 transition">
          <time class="mb-1 text-sm text-gray-500 dark:text-gray-400">{{ item.date }}</time>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">{{ item.title }}</h3>
          <p class="mb-2 text-base text-gray-600 dark:text-gray-300">{{ item.description }}</p>
          <span class="inline-flex items-center px-2 py-1 text-xs font-medium text-white rounded-full"
                :class="statusColor(item.status)">
            {{ item.status }}
          </span>
        </div>
      </li>
    </ol>
  </div>
</template>

<script setup>
const props = defineProps({ events: { type: Array, required: true } })

const statusColor = (status) => {
  switch (status) {
    case "Lengkap": return "bg-green-500"
    case "Belum Lengkap": return "bg-red-500"
    default: return "bg-gray-500"
  }
}
</script>
