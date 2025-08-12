<template>
  <form @submit.prevent="handleSubmit">
    <div class="space-y-4">
      
      <div>
        <label for="nama-tim" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Nama Tim</label>
        <input 
          type="text" 
          id="nama-tim" 
          v-model="form.namaTim"
          :class="{ 'border-red-500': errors.namaTim }"
          class="mt-1 block w-full px-3 py-2 border text-gray-700 dark:text-gray-300 border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          placeholder="Contoh: Tim Neraca 2025"
        />
        <p v-if="errors.namaTim" class="mt-1 text-xs text-red-500">{{ errors.namaTim }}</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="valid-from" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Periode Aktif Mulai</label>
          <input 
            type="date" 
            id="valid-from" 
            v-model="form.validFrom"
            class="mt-1 block w-full px-3 py-2 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
        </div>
        <div>
          <label for="valid-until" class="block text-sm font-medium text-gray-700 dark:text-gray-300">Periode Aktif Selesai</label>
          <input 
            type="date" 
            id="valid-until" 
            v-model="form.validUntil"
            :class="{ 'border-red-500': errors.validUntil }"
            class="mt-1 block w-full px-3 py-2 text-gray-700 dark:text-gray-300 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
          />
          <p v-if="errors.validUntil" class="mt-1 text-xs text-red-500">{{ errors.validUntil }}</p>
        </div>
      </div>

    </div>

    <div class="mt-6 flex justify-end gap-3">
      <button type="button" @click="$emit('close')" class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-md hover:bg-gray-50 dark:hover:bg-gray-600">
        Batal
      </button>
      <button type="submit" class="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700">
        Simpan
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, watchEffect } from 'vue';

const props = defineProps({
  initialData: { type: Object, default: null },
});

const emit = defineEmits(['close', 'submit']);

const form = reactive({
  namaTim: '',
  validFrom: null,
  validUntil: null,
});

const errors = reactive({
  namaTim: null,
  validUntil: null,
});

watchEffect(() => {
  // Reset form dan error setiap kali data berubah
  Object.assign(form, {
    namaTim: '', validFrom: null, validUntil: null
  });
  Object.keys(errors).forEach(key => errors[key] = null);

  if (props.initialData) {
    form.namaTim = props.initialData.namaTim || '';
    form.validFrom = props.initialData.validFrom?.split('T')[0] || null;
    form.validUntil = props.initialData.validUntil?.split('T')[0] || null;
  }
});

const validate = () => {
  // Reset error sebelum validasi baru
  Object.keys(errors).forEach(key => errors[key] = null);
  let isValid = true;

  if (!form.namaTim.trim()) {
    errors.namaTim = 'Nama tim wajib diisi.';
    isValid = false;
  }
  
  if (form.validFrom && form.validUntil && form.validUntil < form.validFrom) {
    errors.validUntil = 'Tanggal selesai tidak boleh sebelum tanggal mulai.';
    isValid = false;
  }
  
  return isValid;
};

const handleSubmit = () => {
  if (validate()) {
    emit('submit', form);
  }
};
</script>