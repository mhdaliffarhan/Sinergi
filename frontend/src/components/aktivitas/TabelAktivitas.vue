<template>
  <div class="overflow-x-auto bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-200 dark:border-gray-700">
    <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
      <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
        <tr>
          <th scope="col" class="px-6 py-3">
            Nama Aktivitas
          </th>
          <th scope="col" class="px-6 py-3 text-center">
            Tim
          </th>
          <th scope="col" class="px-6 py-3 text-center">
            Project
          </th>
          <th scope="col" class="px-6 py-3">
            Jadwal Pelaksanaan
          </th>
        </tr>
      </thead>
      <tbody>
        <tr 
          v-for="item in aktivitas" 
          :key="item.id" 
          @click="goToDetail(item.id)"
          class="border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 cursor-pointer transition-colors">
          <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
            {{ item.namaAktivitas }}
          </th>
          <td class="px-6 py-4 text-center">
            <span class="inline-flex items-center px-2 py-1 text-xs font-medium rounded-full text-white"
              :style="{ backgroundColor: item.team.warna || '#3b82f6' }">
              {{ item.team?.namaTim || '-' }}
            </span>
          </td>
          <td class="px-6 py-4 text-center">
            <span class="inline-flex items-center px-2 py-1 text-xs font-medium rounded-full bg-orange-100 text-orange-600">
              {{ item.project?.namaProject || '-' }}
            </span>
          </td>
          <td class="px-6 py-4 text-center">
            <div class="flex flex-col">
              <span class="flex items-center gap-2">
                <span>🗓️</span>
                <span>{{ formatJadwal(item).tanggal }}</span>
              </span>
              <span v-if="formatJadwal(item).waktu" class="flex items-center gap-2 mt-1 text-xs text-gray-400">
                <span>🕒</span>
                <span>{{ formatJadwal(item).waktu }}</span>
              </span>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const props = defineProps({
  aktivitas: {
    type: Array,
    required: true,
  },
});

const router = useRouter();

// Fungsi untuk navigasi saat baris diklik
const goToDetail = (id) => {
  router.push({ name: 'aktivitas-detail', params: { id: id } });
};

// Fungsi helper untuk memformat tanggal dan waktu
const formatJadwal = (item) => {
  if (!item.tanggalMulai) return { tanggal: '-', waktu: null };

  const options = { day: 'numeric', month: 'short', year: 'numeric' };
  let tanggalTampil = '';
  let waktuTampil = null;

  const tglMulai = new Date(item.tanggalMulai);
  
  if (item.tanggalSelesai) {
    const tglSelesai = new Date(item.tanggalSelesai);
    tanggalTampil = `${tglMulai.toLocaleDateString('id-ID', options)} - ${tglSelesai.toLocaleDateString('id-ID', options)}`;
  } else {
    tanggalTampil = tglMulai.toLocaleDateString('id-ID', options);
  }

  if (item.jamMulai) {
    waktuTampil = `${item.jamMulai} - ${item.jamSelesai} WITA`;
  }

  return { tanggal: tanggalTampil, waktu: waktuTampil };
};
</script>