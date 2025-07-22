<template>
  <div>
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-green-700 dark:text-green-400">Dashboard Aktivitas</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Ringkasan visual kelengkapan dokumen dan aktivitas.</p>
      </div> 
      <div class="mt-4 sm:mt-0">
        <label for="team-filter" class="sr-only">Filter berdasarkan Tim</label>
        <select 
          id="team-filter" 
          v-model="selectedTeam"
          class="block p-1 w-full sm:w-auto rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
        >
          <option v-for="team in teamList" :key="team" :value="team">{{ team }}</option>
        </select>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="lg:col-span-1 bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
        <h3 class="font-semibold text-gray-800 dark:text-white mb-4">Kelengkapan Aktivitas</h3>
        <ActivityCompletionChart :series="completionData.series" :labels="completionData.labels" />
      </div>


      <div class="lg:col-span-2 bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
        <h3 class="font-semibold text-gray-800 dark:text-white mb-4">Aktivitas per Tim</h3>
        <TeamActivityBarChart :series="teamActivityData.series" :categories="teamActivityData.categories" />
      </div>
      
      <div class="lg:col-span-3 bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md">
        <h3 class="font-semibold text-gray-800 dark:text-white mb-4">Progres dari Waktu ke Waktu</h3>
        <ProgressLineChart :series="progressOverTimeData.series" :categories="progressOverTimeData.categories" />
      </div>
    </div>

    <div class="mt-8">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-white mb-4">Daftar Aktivitas Belum Lengkap</h3>
      <IncompleteActivitiesTable :activities="incompleteActivities" />
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import ActivityCompletionChart from '@/components/charts/ActivityCompletionChart.vue';
import TeamActivityBarChart from '@/components/charts/TeamActivityBarChart.vue';
import ProgressLineChart from '@/components/charts/ProgressLineChart.vue';
import IncompleteActivitiesTable from '@/components/aktivitas/IncompleteActivitiesTable.vue';

const router = useRouter();
const activities = ref([]);

const selectedTeam = ref('Semua Tim');

const fetchDashboardData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/aktivitas');
    // Kita gunakan lagi fungsi konversi yang sudah ada
    activities.value = convertKeysToCamelCase(response.data);
    console.log(response.data);
  } catch (error) {
    console.error("Gagal mengambil data untuk dashboard:", error);
  }
};

onMounted(() => {
  fetchDashboardData();
});

const snakeToCamel = (str) => str.replace(/([-_][a-z])/g, (group) => group.toUpperCase().replace('-', '').replace('_', ''));
const convertKeysToCamelCase = (obj) => {
  if (obj === null || typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map(item => convertKeysToCamelCase(item));
  const newObj = {};
  for (let key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      newObj[snakeToCamel(key)] = convertKeysToCamelCase(obj[key]);
    }
  }
  return newObj;
};

const teamList = computed(() => {
  const teams = new Set(activities.value.map(a => a.timPenyelenggara));
  return ['Semua Tim', ...teams];
});

const filteredActivities = computed(() => {
  if (selectedTeam.value === 'Semua Tim') {
    return activities.value; // Tampilkan semua jika 'Semua Tim' dipilih
  }
  return activities.value.filter(a => a.timPenyelenggara === selectedTeam.value);
});

const isActivityComplete = (activity) => {
  if (activity.daftarDokumenWajib.length === 0) return true;
  return activity.daftarDokumenWajib.every(doc => doc.status === 'Selesai');
};

const completionData = computed(() => {
  let completedCount = 0;
  let inProgressCount = 0;
  // Gunakan filteredActivities di sini
  filteredActivities.value.forEach(activity => {
    if (isActivityComplete(activity)) completedCount++;
    else inProgressCount++;
  });
  return { series: [completedCount, inProgressCount], labels: ['Selesai', 'Belum Lengkap'] };
});

const teamActivityData = computed(() => {
  const teams = {};
  // Gunakan filteredActivities di sini (jika tidak "Semua Tim")
  const sourceData = selectedTeam.value === 'Semua Tim' ? activities.value : filteredActivities.value;
  sourceData.forEach(activity => {
    const teamName = activity.timPenyelenggara;
    if (!teams[teamName]) {
      teams[teamName] = { completed: 0, inProgress: 0 };
    }
    if (isActivityComplete(activity)) teams[teamName].completed++;
    else teams[teamName].inProgress++;
  });
  const categories = Object.keys(teams);
  const series = [
    { name: 'Selesai', data: categories.map(team => teams[team].completed) },
    { name: 'Belum Lengkap', data: categories.map(team => teams[team].inProgress) },
  ];
  return { series, categories };
});

const progressOverTimeData = computed(() => {
  const dates = {};

  // Fungsi untuk mengambil bagian tanggal saja (YYYY-MM-DD)
  const getOnlyDate = (dateString) => dateString ? dateString.split('T')[0] : null;

  // Mengumpulkan data (tidak berubah banyak, hanya normalisasi tanggal)
  filteredActivities.value.forEach(activity => {
    const date = getOnlyDate(activity.dibuatPada);
    if (date) {
        if (!dates[date]) dates[date] = { activitiesCreated: 0, documentsUploaded: 0 };
        dates[date].activitiesCreated++;
    }
  });
  filteredActivities.value.forEach(activity => {
    activity.dokumen.forEach(doc => {
      if (doc.diunggahPada) {
        const date = getOnlyDate(doc.diunggahPada);
        if (date) {
            if (!dates[date]) dates[date] = { activitiesCreated: 0, documentsUploaded: 0 };
            dates[date].documentsUploaded++;
        }
      }
    });
  });

  const sortedDates = Object.keys(dates).sort();
  
  const series = [
    { name: 'Aktivitas Dibuat', data: sortedDates.map(date => dates[date].activitiesCreated) },
    { name: 'Dokumen Diunggah', data: sortedDates.map(date => dates[date].documentsUploaded) },
  ];

  // --- PERUBAHAN UTAMA DI SINI ---
  // Format label tanggal (categories) menjadi DD/MM/YY
  const formattedCategories = sortedDates.map(dateString => 
    new Date(dateString).toLocaleDateString('id-ID', {
      day: '2-digit',
      month: '2-digit',
      year: '2-digit'
    })
  );
  
  return { series, categories: formattedCategories };
});

const incompleteActivities = computed(() => {
  // Gunakan filteredActivities di sini
  return filteredActivities.value.filter(activity => !isActivityComplete(activity));
});

const goToDetail = (id) => {
  router.push({ name: 'aktivitas-detail', params: { id: id } });
};

</script>