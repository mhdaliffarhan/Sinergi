<template>
  <form @submit.prevent="handleSubmit">
    <div class="space-y-4">
      <div class="p-3 border border-gray-200 dark:border-gray-600 rounded-md bg-gray-50 dark:bg-gray-900/50">
        <p class="text-xs font-medium text-gray-500 dark:text-gray-400">Nama File:</p>
        <p class="text-sm font-semibold text-gray-800 dark:text-gray-200 truncate">{{ file.name }}</p>
      </div>
      
      <div>
        <label for="checklist-item" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Penuhi Checklist (Opsional)</label>
        <select 
          id="checklist-item" 
          v-model="selectedChecklistItemId"
          class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
        >
          <option value="lainnya">Dokumen Lainnya (tidak ada di checklist)</option>
          <option v-for="item in unfulfilledItems" :key="item.id" :value="item.id">
            {{ item.namaDokumen }}
          </option>
        </select>
      </div>

      <Transition name="fade">
        <div v-if="selectedChecklistItemId === 'lainnya'">
          <label for="keterangan" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Keterangan</label>
          <input 
            type="text" 
            id="keterangan" 
            v-model="keterangan"
            required
            class="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm dark:bg-gray-700 dark:text-white"
            placeholder="Contoh: Surat Tugas Tambahan"
          />
        </div>
      </Transition>
    </div>

    <div class="mt-6 flex justify-end gap-3">
      <button type="button" @click="$emit('close')" class="px-4 py-2 text-sm font-medium text-gray-700 bg-white dark:bg-gray-700 dark:text-gray-200 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none">Batal</button>
      <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 border border-transparent rounded-md shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">Unggah & Simpan</button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  file: { type: Object, required: true },
  unfulfilledItems: { type: Array, default: () => [] }
});
const emit = defineEmits(['submit', 'close']);

const selectedChecklistItemId = ref('lainnya');
const keterangan = ref('');

const handleSubmit = () => {
  let finalKeterangan = '';

  // Tentukan nilai 'keterangan' berdasarkan pilihan dropdown
  if (selectedChecklistItemId.value === 'lainnya') {
    finalKeterangan = keterangan.value;
  } else {
    const selectedItem = props.unfulfilledItems.find(item => item.id === selectedChecklistItemId.value);
    if (selectedItem) {
      finalKeterangan = selectedItem.namaDokumen;
    }
  }

  // Validasi sebelum mengirim
  if (finalKeterangan.trim()) {
    emit('submit', { 
      keterangan: finalKeterangan, 
      file: props.file,
      checklistItemId: selectedChecklistItemId.value === 'lainnya' ? null : selectedChecklistItemId.value
    });
  } else {
    alert('Keterangan wajib diisi atau dipilih dari checklist.');
  }
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>