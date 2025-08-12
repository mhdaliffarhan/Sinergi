<template>
    <div class="flex-shrink-0 border-b border-gray-200 dark:border-gray-700">
      <nav class="flex space-x-6" aria-label="Tabs">
        <button 
          @click="activeTab = 'detail'"
          :class="[activeTab === 'detail' ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:hover:text-gray-200']"
          class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
        >
          Detail Tim
        </button>
        <button 
          @click="activeTab = 'anggota'"
          :class="[activeTab === 'anggota' ? 'border-blue-500 text-blue-600 dark:text-blue-400' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:hover:text-gray-200']"
          class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
        >
          Anggota Tim
        </button>
      </nav>
    </div>

    <div class="flex-grow pt-6 overflow-y-auto">
      <div v-if="activeTab === 'detail'">
        <FormTim
          :initial-data="team"
          @submit="handleUpdate"
          :is-edit-mode="true"
        />
      </div>

      <div v-if="activeTab === 'anggota'">
        <p class="text-center text-gray-500 dark:text-gray-400">
          Fitur untuk mengelola anggota tim akan dibuat di sini.
        </p>
      </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import FormTim from '@/components/admin/FormTim.vue';

const props = defineProps({
  team: { type: Object, required: true }
});

const emit = defineEmits(['close', 'teamUpdated']);

const activeTab = ref('detail');

// Fungsi ini akan meneruskan data yang diubah ke parent
const handleUpdate = (formData) => {
  emit('teamUpdated', { ...formData, id: props.team.id });
};
</script>