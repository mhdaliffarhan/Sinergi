<template>
  <div class="space-y-6">
    <div class="bg-white dark:bg-gray-800 shadow-md rounded-xl p-4 transition hover:shadow-lg">
      <div class="flex flex-col gap-6">

        <div class="flex items-center gap-3">
          <label class="font-semibold text-gray-700 dark:text-gray-200 shrink-0">Pilih Pegawai:</label>
          
          <div class="relative w-full sm:w-64">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Cari pegawai..."
              class="border rounded-lg px-3 py-1.5 w-full dark:bg-gray-700 dark:text-gray-100 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
              @focus="showDropdown = true"
              @blur="handleBlur"
            />
            <div 
              v-if="showDropdown && filteredPegawai.length > 0" 
              class="absolute z-20 mt-1 w-full bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg shadow-lg max-h-60 overflow-y-auto"
            >
              <div
                class="px-3 py-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200"
                :class="{'bg-gray-200 dark:bg-gray-600': selectedPegawaiId === ''}"
                @mousedown.prevent="selectPegawai({ id: '' })"
              >
                Semua Pegawai
              </div>
              <div 
                v-for="pegawai in filteredPegawai" 
                :key="pegawai.id"
                class="px-3 py-2 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200"
                :class="{'bg-gray-200 dark:bg-gray-600': selectedPegawaiId === pegawai.id}"
                @mousedown.prevent="selectPegawai(pegawai)"
              >
                {{ pegawai.namaLengkap }}
              </div>
            </div>
          </div>
        </div>

        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div class="flex items-center gap-3">
            <label class="font-semibold text-gray-700 dark:text-gray-200 shrink-0">Mode Tampilan:</label>
            <div class="relative inline-flex items-center bg-gray-100 dark:bg-gray-700 p-1 rounded-lg">
              <span 
                class="absolute top-1 bottom-1 left-1 w-[calc(50%-0.25rem)] bg-orange-500 rounded-md shadow-md transition-transform duration-300 ease-in-out" 
                :class="{ 'translate-x-full': mode === 'timeline' }" 
              ></span>
              <button 
                @click="mode = 'calendar'" 
                title="Tampilan Kalender" 
                class="relative z-10 w-1/2 px-3 py-1.5 flex justify-center items-center transition-colors duration-300" 
                :class="mode === 'calendar' ? 'text-white' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'" 
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path></svg>
              </button>
              <button 
                @click="mode = 'timeline'" 
                title="Tampilan Timeline" 
                class="relative z-10 w-1/2 px-3 py-1.5 flex justify-center items-center transition-colors duration-300" 
                :class="mode === 'timeline' ? 'text-white' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'" 
              >
                <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"></path></svg>
              </button>
            </div>
          </div>
          <div v-if="mode === 'timeline'" class="flex gap-2 items-center">
            <button @click="prevMonth" class="px-2 py-1 rounded-lg bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-500">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
            </button>
            <span class="font-semibold text-gray-700 dark:text-gray-200">{{ format(timelineStartDate, 'MMMM yyyy', { locale: idLocale }) }}</span>
            <button @click="nextMonth" class="px-2 py-1 rounded-lg bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-500">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path></svg>
            </button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="mode === 'calendar'" class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow">
      <FullCalendar :options="calendarOptions" />
    </div>

    <div v-else class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow overflow-x-auto">
      <div class="inline-block min-w-full">
        <table class="w-full timeline-table">
          <thead>
            <tr>
              <th class="border-b-2 dark:border-gray-700 px-4 py-2 text-left text-sm font-semibold dark:text-gray-200 sticky left-0 bg-white dark:bg-gray-800 z-10 timeline-header">Pegawai</th>
              <th v-for="date in timelineDates" :key="date" class="border-b-2 dark:border-gray-700 px-2 py-2 text-center text-xs font-semibold dark:text-gray-200 timeline-date-header">
                {{ format(new Date(date), 'dd MMM') }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="pegawai in daftarPegawaiTimeline" :key="pegawai.id">
              <td class="border-b dark:border-gray-700 px-4 py-2 text-sm dark:text-gray-300 sticky left-0 bg-white dark:bg-gray-800 z-10 timeline-row-header">{{ pegawai.namaLengkap }}</td>
              <td 
                v-for="date in timelineDates" 
                :key="date" 
                class="border-b dark:border-gray-700 px-2 py-2 relative"
              >
                <div v-for="event in getEventsForDayAndPegawai(date, pegawai.id)" :key="event.id"
                  class="absolute inset-y-0 left-0 right-0 m-1 rounded-full flex items-center justify-center p-1 text-white text-xs whitespace-nowrap overflow-hidden transition-all duration-300 timeline-event-bar"
                  :style="{
                    'background-color': event.backgroundColor,
                    'width': calculateEventWidth(event),
                    'transform': 'translateX(' + calculateEventOffset(event) + ')'
                  }"
                  :title="event.title + ' (' + event.start + ' - ' + event.end + ')'"
                  @click="goToActivityDetail(event.id)"
                >
                  {{ event.title }}
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from 'vue-router';
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import idLocale from 'date-fns/locale/id';
import axios from "axios";
import { useToast } from 'vue-toastification';
import { format, eachDayOfInterval, isWithinInterval, addMonths, subMonths, startOfMonth, endOfMonth, addDays } from 'date-fns';

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const toast = useToast();
const router = useRouter();

const mode = ref("calendar");
const selectedPegawaiId = ref("");
const aktivitas = ref([]);
const allPegawai = ref([]);
const searchQuery = ref("");
const showDropdown = ref(false);
const timelineStartDate = ref(startOfMonth(new Date()));

const prevMonth = () => { timelineStartDate.value = subMonths(timelineStartDate.value, 1); };
const nextMonth = () => { timelineStartDate.value = addMonths(timelineStartDate.value, 1); };

onMounted(async () => {
  try {
    const [aktivitasResponse, pegawaiResponse] = await Promise.all([
      axios.get(`${apiUrl}/api/aktivitas`),
      axios.get(`${apiUrl}/api/users?limit=1000`)
    ]);
    aktivitas.value = aktivitasResponse.data;
    allPegawai.value = pegawaiResponse.data.items.sort((a, b) => a.namaLengkap.localeCompare(b.namaLengkap));

    const kepala = allPegawai.value.find(p => p.jabatanId === 1);
    if (kepala) {
      selectedPegawaiId.value = kepala.id;
    }
  } catch (err) {
    console.error("Gagal mengambil data:", err);
    toast.error("Gagal mengambil data pegawai atau aktivitas.");
  }
});

const filteredPegawai = computed(() => {
  if (!searchQuery.value) {
    return allPegawai.value;
  }
  const query = searchQuery.value.toLowerCase();
  return allPegawai.value.filter(p => p.namaLengkap.toLowerCase().includes(query));
});

const selectPegawai = (pegawai) => {
  selectedPegawaiId.value = pegawai.id;
  searchQuery.value = pegawai.id ? pegawai.namaLengkap : "";
  showDropdown.value = false;
};

const handleBlur = () => {
  setTimeout(() => { showDropdown.value = false; }, 200);
};

const filteredActivities = computed(() => {
  let data = aktivitas.value;
  if (selectedPegawaiId.value) {
    data = data.filter(a => a.users && a.users.some(u => u.id === selectedPegawaiId.value));
  }
  return data;
});

const daftarPegawaiTimeline = computed(() => {
  if (selectedPegawaiId.value) {
    return allPegawai.value.filter(p => p.id === selectedPegawaiId.value);
  }
  const pegawaiMap = new Map();
  filteredActivities.value.forEach(a => {
    if (a.users) {
      a.users.forEach(u => {
        pegawaiMap.set(u.id, u);
      });
    }
  });
  return Array.from(pegawaiMap.values()).sort((a, b) => a.namaLengkap.localeCompare(b.namaLengkap));
});

const calendarEvents = computed(() => 
  filteredActivities.value.map(a => {
    let endDate = a.tanggalSelesai;
    if (endDate) {
      const date = new Date(endDate);
      date.setDate(date.getDate() + 1);
      endDate = date.toISOString().split('T')[0];
    }
    return {
      id: a.id,
      title: a.namaAktivitas,
      start: a.tanggalMulai,
      end: endDate,
      backgroundColor: a.team?.warna || '#2563eb',
      borderColor: a.team?.warna || '#2563eb',
      textColor: '#fff'
    };
  })
);

const calendarOptions = computed(() => ({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: "dayGridMonth",
  events: calendarEvents.value,
  eventClick: (info) => {
    const id = info.event.id;
    router.push(`/aktivitas/detail/${id}`);
  },
  locale: idLocale,
  buttonText: { today: 'Hari Ini' },
}));

const timelineDates = computed(() => {
  const start = startOfMonth(timelineStartDate.value);
  const end = endOfMonth(timelineStartDate.value);
  const dates = eachDayOfInterval({ start, end }).map(date => date.toISOString().split('T')[0]);

  console.log("🟢 timelineStartDate:", timelineStartDate.value);
  console.log("🟢 start:", start, "end:", end);
  console.log("🟢 timelineDates:", dates);

  return dates;
});

const getEventsForDayAndPegawai = (date, pegawaiId) => {
  const day = new Date(date);
  return filteredActivities.value.filter(a => {
    const eventStart = new Date(a.tanggalMulai);
    const eventEnd = a.tanggalSelesai ? new Date(a.tanggalSelesai) : eventStart;
    return a.users && a.users.some(u => u.id === pegawaiId) && isWithinInterval(day, { start: eventStart, end: eventEnd });
  }).map(a => ({
    id: a.id,
    title: a.namaAktivitas,
    start: a.tanggalMulai,
    end: a.tanggalSelesai,
    backgroundColor: a.team?.warna || '#2563eb'
  }));
};

const calculateEventWidth = (event) => {
  if (!event.start || !event.end) return '100%';
  const start = new Date(event.start);
  const end = addDays(new Date(event.end), 1);
  const timelineStart = new Date(timelineDates.value[0]);
  const timelineEnd = addDays(new Date(timelineDates.value[timelineDates.value.length - 1]), 1);
  const totalDuration = timelineEnd.getTime() - timelineStart.getTime();
  const eventDuration = end.getTime() - start.getTime();
  const width = (eventDuration / totalDuration) * 100;
  return `${width}%`;
};

const calculateEventOffset = (event) => {
  if (!event.start) return '0';
  const eventStart = new Date(event.start);
  const timelineStart = new Date(timelineDates.value[0]);
  const offsetDuration = eventStart.getTime() - timelineStart.getTime();
  const timelineEnd = addDays(new Date(timelineDates.value[timelineDates.value.length - 1]), 1);
  const totalDuration = timelineEnd.getTime() - timelineStart.getTime();
  const offset = (offsetDuration / totalDuration) * 100;
  return `${offset}%`;
};

const goToActivityDetail = (id) => {
  router.push(`/aktivitas/detail/${id}`);
};
</script>