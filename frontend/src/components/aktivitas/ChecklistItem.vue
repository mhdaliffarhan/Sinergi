<template>
  <div>
    <div v-if="!item.dokumenTerkait" class="flex flex-col sm:flex-row items-start sm:items-center sm:justify-between p-3 rounded-lg bg-yellow-50 dark:bg-yellow-900/30 border-l-4 border-yellow-400 gap-3">
      <span class="text-sm font-medium text-gray-800 dark:text-gray-200">{{ item.namaDokumen }}</span>
      <div class="flex items-center gap-2 w-full sm:w-auto">
        <span class="text-xs font-semibold px-2.5 py-1 rounded-full bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300">
          Wajib Diunggah
        </span>
        <button v-if="isAnggotaTim" @click="$emit('unggah', item.id)" class="px-3 py-1 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 w-full sm:w-auto">
          Unggah
        </button>
      </div>
    </div>
    
    <div 
      v-else
      class="flex items-center p-3 rounded-lg border-l-4 transition-all duration-300 gap-4"
      :class="item.statusPengecekan 
        ? 'bg-green-50 dark:bg-green-900/30 border-green-500' 
        : 'bg-gray-50 dark:bg-gray-800/60 border-transparent hover:border-gray-300 dark:hover:border-gray-600'"
    >
      <div class="flex-shrink-0">
        <button
          type="button"
          @click="canChecklist && $emit('cek', { id: item.id, value: !item.statusPengecekan })"
          :disabled="!canChecklist"
          class="w-7 h-7 rounded-lg border-2 flex items-center justify-center transition-all duration-200 ease-in-out transform hover:scale-110"
          :class="[
            item.statusPengecekan 
              ? 'bg-green-600 border-green-600' 
              : 'bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-500',
            canChecklist 
              ? 'cursor-pointer focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800' 
              : 'cursor-not-allowed opacity-60'
          ]"
          :title="canChecklist ? (item.statusPengecekan ? 'Batalkan tanda cek' : 'Tandai sudah dicek') : 'Hanya ketua tim atau project leader yang bisa mengubah'"
        >
          <svg v-if="item.statusPengecekan" class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3">
            <path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7" />
          </svg>
        </button>
      </div>
      
      <DokumenItem 
        :dokumen="item.dokumenTerkait"
        :isAnggotaTim="isAnggotaTim"
        @hapus="$emit('hapus', item.dokumenTerkait.id)"
        @preview="$emit('preview', item.dokumenTerkait)"
        class="flex-grow"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import DokumenItem from '@/components/aktivitas/DokumenItem.vue';

const props = defineProps({
  item: { type: Object, required: true },
  isKetuaTim: { type: Boolean, default: false },
  isProjectLeader: {type: Boolean, default: false},
  isAnggotaTim: { type: Boolean, default: false},
});

const canChecklist = computed(() => props.isKetuaTim || props.isProjectLeader);

defineEmits(['unggah', 'hapus', 'preview' ,'cek']);
</script>