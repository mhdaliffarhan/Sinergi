<template>
  <router-link 
    :to="{ name: 'aktivitas-detail', params: { id: id } }"  
    class="block p-4 mb-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-200"
  >
    <h3 class="text-lg font-semibold text-gray-800 dark:text-gray-100 mb-2">
      {{ namaAktivitas }}
    </h3>

    <div class="flex items-center gap-4 text-sm text-gray-500 dark:text-gray-400 mb-3">
      <div class="flex items-center gap-1">
        <span>📅</span>
        <span>{{ formattedTanggal }}</span>
      </div>
      <div class="flex items-center gap-1">
        <span class="inline-flex items-center px-2 py-1 text-xs font-medium rounded-full text-white"
              :style="{ backgroundColor: team.warna || '#3b82f6' }">
              👥 {{ team?.namaTim || '-' }}
        </span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed} from 'vue';

const props = defineProps({
  id: { type: Number, required: true },
  namaAktivitas: { type: String, required: true },
  team: {
    type: Object, 
    required: true, 
  },
  tanggalMulai: { type: String },
  tanggalSelesai: { type: String },
  jamMulai: { type: String },
  jamSelesai: { type: String },
});

const formattedTanggal = computed(() => {
  let tanggalTampil = '';
  const options = { day: 'numeric', month: 'long', year: 'numeric' };

  if (props.tanggalMulai && props.tanggalSelesai) {
    const mulai = new Date(props.tanggalMulai).toLocaleDateString('id-ID', { day: 'numeric', month: 'long' });
    const selesai = new Date(props.tanggalSelesai).toLocaleDateString('id-ID', options);
    tanggalTampil = `${mulai} - ${selesai}`;
  } else if (props.tanggalMulai) {
    tanggalTampil = new Date(props.tanggalMulai).toLocaleDateString('id-ID', options);
  }

  if (props.jamMulai && props.jamSelesai) {
    tanggalTampil += ` | ${props.jamMulai} - ${props.jamSelesai}`;
  }

  return tanggalTampil || 'Tanggal tidak ditentukan';
});
</script>