<template>
  <div class="space-y-6">
    <div class="bg-white dark:bg-gray-800 shadow-md rounded-xl p-4 transition hover:shadow-lg">
      <div class="flex flex-col gap-6">
        
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div class="flex items-center gap-3 w-full sm:w-auto">
            
            <div class="relative flex items-center bg-gray-100 dark:bg-gray-700 p-1 rounded-lg w-full sm:w-auto">
              
              <span
                class="absolute top-1 bottom-1 left-1 w-1/3 bg-orange-500 rounded-md shadow-md transition-transform duration-300 ease-in-out"
                :class="{
                  'translate-x-0': mode === 'team',
                  'translate-x-full': mode === 'timeline',
                  'translate-x-[200%]': mode === 'person'
                }"
              ></span>

              <button
                @click="mode = 'team'"
                title="Kalender Tim"
                class="relative z-10 w-1/3 px-4 py-1.5 flex justify-center items-center transition-colors duration-300 rounded-md"
                :class="mode === 'team' ? 'text-white' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'"
              >
                <span class="text-xl">👥</span>
              </button>

              <button
                @click="mode = 'timeline'"
                title="Tampilan Timeline"
                class="relative z-10 w-1/3 px-4 py-1.5 flex justify-center items-center transition-colors duration-300 rounded-md"
                :class="mode === 'timeline' ? 'text-white' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'"
              >
                <span class="text-xl">📊</span>
              </button>
              
              <button
                @click="mode = 'person'"
                title="Kalender per Orang"
                class="relative z-10 w-1/3 px-4 py-1.5 flex justify-center items-center transition-colors duration-300 rounded-md"
                :class="mode === 'person' ? 'text-white' : 'text-gray-500 hover:text-gray-800 dark:hover:text-gray-200'"
              >
                <span class="text-xl">👤</span>
              </button>
            </div>
          </div>

          <div v-if="mode === 'team' || mode === 'timeline'" class="flex flex-wrap gap-2 mt-4 sm:mt-0">
            <button
              @click="selectAllTeams()"
              class="px-3 py-1.5 text-sm font-medium rounded-lg transition-colors duration-200"
              :class="{
                'bg-blue-600 text-white shadow': selectedTeams.length === 0,
                'bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-500': selectedTeams.length > 0
              }"
            >
              Semua
            </button>
            <button
              v-for="team in teams"
              :key="team.id"
              @click="toggleTeam(team)"
              class="px-3 py-1.5 text-sm font-medium rounded-lg transition-colors duration-200"
              :style="isTeamSelected(team) ? { backgroundColor: team.warna, color: 'white' } : {}"
              :class="{
                'shadow': isTeamSelected(team),
                'bg-gray-200 dark:bg-gray-600 text-gray-800 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-500': !isTeamSelected(team)
              }"
            >
              {{ team.namaTim }}
            </button>
          </div>

          <div v-if="mode === 'person'" class="flex items-center gap-3 w-full sm:w-auto">
            <div class="relative w-full sm:w-64">
              <input
                type="text"
                v-model="searchQuery"
                placeholder="Cari pegawai..."
                class="border rounded-lg px-3 py-1.5 w-full dark:bg-gray-700 dark:text-gray-100  border-gray-200 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
        </div>
      </div>
    </div>

    <div v-if="mode === 'team' || mode === 'person'" class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow">
      <div ref="calendar" class="w-full"></div>
    </div>
    
    <div v-else-if="mode === 'timeline'" class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow overflow-hidden relative">
      <div class="flex flex-col h-full">
        <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center p-2 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 sticky top-0 z-20">
          <h2 class="text-xl font-bold text-gray-800 dark:text-gray-100">Timeline Anggota Tim</h2>
          <div class="flex gap-2 items-center">
            <button @click="prevMonth" class="px-2 py-1 rounded-lg bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-500">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd"></path></svg>
            </button>
            <span class="font-semibold text-gray-700 dark:text-gray-200">{{ format(timelineCurrentDate, 'MMMM yyyy', { locale: idLocale }) }}</span>
            <button @click="nextMonth" class="px-2 py-1 rounded-lg bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-200 hover:bg-gray-300 dark:hover:bg-gray-500">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"></path></svg>
            </button>
          </div>
        </div>

        <div class="flex-grow flex-col relative overflow-x-auto scrollbar-hide timeline-scroll-container">
          <div class="flex sticky top-0 z-10 w-full bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
            <div class="timeline-header-label-col text-center sticky left-0 z-30 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
              Pegawai
            </div>
            <div 
              v-for="day in timelineDates" 
              :key="day" 
              class="timeline-header-day-col"
              :class="{ 'bg-weekend-light dark:bg-weekend-dark': isWeekend(day) }"
            >
              <span class="block text-xs text-gray-500 dark:text-gray-400">
                {{ format(new Date(day), 'E', { locale: idLocale }) }}
              </span>
              <span class="block text-sm font-bold text-gray-700 dark:text-gray-200">
                {{ format(new Date(day), 'dd') }}
              </span>
            </div>
          </div>
          
          <div class="flex-grow timeline-content-body">
            <div v-for="pegawai in daftarPegawaiTimeline" :key="pegawai.id" class="flex timeline-row-wrap relative">
              <div class="timeline-row-label sticky left-0 z-20 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
                <span class="truncate">{{ pegawai.namaLengkap }}</span>
              </div>
              <div 
                class="relative timeline-row-content "
                :style="{ height: `${getMaxLane(pegawai.id) * 38 + 12}px` }"
              >
                <div v-for="day in timelineDates" :key="day"
                  class="absolute top-0 bottom-0 border-l border-gray-200 dark:border-gray-700 dark:bg-gray-800"
                  :style="{
                    left: `${timelineDates.indexOf(day) * 50}px`,
                    width: '50px',
                  }"
                ></div>
                <div class="absolute bottom-0 left-0 right-0 h-px bg-gray-200 dark:bg-gray-700"></div>

                <div 
                  v-for="event in getEventsForPegawai(pegawai.id)" 
                  :key="event.id"
                  class="timeline-event-bar group"
                  :style="{
                    'background-color': event.backgroundColor,
                    'left': `${calculateEventOffset(event)}px`,
                    'width': `${calculateEventWidth(event)}px`,
                    'top': `${(event.lane - 1) * 38 + 6}px`
                  }"
                  @click="goToActivityDetail(event.id)"
                >
                  <span class="event-title-text">{{ event.title }}</span>
                  <div class="event-tooltip">
                    <span class="font-bold text-white">{{ event.title }}</span>
                    <span class="text-xs text-gray-200">
                      <template v-if="event.start_time && event.end_time">
                        ({{ event.start_time }} - {{ event.end_time }} WITA)
                      </template>
                      <template v-else>
                        (Sepanjang Hari)
                      </template>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <ModalAktivitas v-if="isModalOpen" :aktivitas="selectedAktivitas" @close="closeModal" @go-to-detail="goToActivityDetail" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from "vue";
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { Calendar } from "@fullcalendar/core";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import timeGridPlugin from "@fullcalendar/timegrid";
import { id as idLocale } from 'date-fns/locale'; 
import axios from "axios";
import { useToast } from 'vue-toastification';
import { format, eachDayOfInterval, isWithinInterval, addDays, subMonths, addMonths, startOfMonth, endOfMonth, parseISO, differenceInDays } from 'date-fns';

import ModalAktivitas from '@/components/aktivitas/ModalAktivitas.vue';

const baseURL = import.meta.env.VITE_API_BASE_URL;
const toast = useToast();
const router = useRouter();
const authStore = useAuthStore();

const mode = ref("team");
const selectedTeams = ref([]); 
const selectedPegawaiId = ref(null);
const allPegawai = ref([]);
const searchQuery = ref("");
const showDropdown = ref(false);

const teams = ref([]);
const aktivitas = ref([]);
const timelineCurrentDate = ref(new Date());

const calendar = ref(null);
let fullCalendarInstance = null;

const isKepalaKantor = computed(() => authStore.user?.jabatan?.namaJabatan === 'Kepala Kantor');

const prevMonth = () => { timelineCurrentDate.value = subMonths(timelineCurrentDate.value, 1); };
const nextMonth = () => { timelineCurrentDate.value = addMonths(timelineCurrentDate.value, 1); };

const isWeekend = (dateString) => {
  const date = new Date(dateString);
  const day = date.getDay();
  return day === 0 || day === 6;
};

const assignLanes = (events) => {
  const sortedEvents = [...events].sort((a, b) => new Date(a.start) - new Date(b.start));
  const lanes = [];
  sortedEvents.forEach(event => {
    let assignedLane = -1;
    for (let i = 0; i < lanes.length; i++) {
      let canFit = true;
      for (const placedEvent of lanes[i]) {
        const start1 = new Date(event.start);
        const end1 = event.end ? new Date(event.end) : start1;
        const start2 = new Date(placedEvent.start);
        const end2 = placedEvent.end ? new Date(placedEvent.end) : start2;
        if (Math.max(start1.getTime(), start2.getTime()) <= Math.min(end1.getTime(), end2.getTime())) {
          canFit = false;
          break;
        }
      }
      if (canFit) {
        assignedLane = i;
        break;
      }
    }
    if (assignedLane === -1) {
      lanes.push([event]);
      event.lane = lanes.length;
    } else {
      lanes[assignedLane].push(event);
      event.lane = assignedLane + 1;
    }
  });
  return sortedEvents;
};

const getMaxLane = (pegawaiId) => {
  const events = getEventsForPegawai(pegawaiId);
  console.log("Maksimal Baris untuk pegawai dengan ID : ",pegawaiId, " adalah ", events.length > 0 ? Math.max(...events.map(e => e.lane)) : 1)
  return events.length > 0 ? Math.max(...events.map(e => e.lane)) : 1;
};

const fetchInitialData = async () => {
  try {
    const [teamsResponse, usersResponse] = await Promise.all([
      axios.get(`${baseURL}/api/teams?limit=1000`),
      axios.get(`${baseURL}/api/users?limit=1000`)
    ]);
    teams.value = teamsResponse.data.items;
    allPegawai.value = usersResponse.data.items.sort((a, b) => a.namaLengkap.localeCompare(b.namaLengkap));

    const kepala = allPegawai.value.find(p => p.jabatan?.namaJabatan === "Kepala Kantor");
    if (kepala) {
      selectedPegawaiId.value = kepala.id;
    }
  } catch (err) {
    console.error("Gagal mengambil data awal:", err);
    toast.error("Gagal mengambil data tim atau pegawai.");
  }
};

const fetchAktivitas = async () => {
  try {
    let endpoint = `${baseURL}/api/aktivitas`; // Endpoint default
    let params = {};

    if (mode.value === 'team' || mode.value === 'timeline') {
      // Jika filter tim, gunakan endpoint events
      endpoint = `${baseURL}/api/kalender/events`;
      const teamIds = selectedTeams.value.map(t => t.id).join(',');
      if (teamIds) params.team_ids = teamIds;
    } else if (mode.value === 'person' && selectedPegawaiId.value) {
      // Jika filter per orang, gunakan endpoint users/aktivitas
      endpoint = `${baseURL}/api/users/${selectedPegawaiId.value}/aktivitas`;
    }
    
    const response = await axios.get(endpoint, { params });
    aktivitas.value = response.data;
  } catch (err) {
    console.error("Gagal mengambil data aktivitas:", err);
    toast.error("Gagal mengambil data aktivitas.");
  }
};

const filteredActivities = computed(() => {
  let data = aktivitas.value;

  // Kondisi 1: Mode Tim
  if (mode.value === 'team') {
    // Filter aktivitas berdasarkan tim yang dipilih
    if (selectedTeams.value.length > 0) {
      const teamIds = new Set(selectedTeams.value.map(t => t.id));
      data = data.filter(a => a.teamId && teamIds.has(a.teamId));
    }
  } 
  // Kondisi 2: Mode Timeline atau Person
  else if (mode.value === 'timeline' || mode.value === 'person') {
    // Ambil semua ID pegawai yang relevan
    const relevantPegawaiIds = new Set(daftarPegawaiTimeline.value.map(p => p.id));

    if (relevantPegawaiIds.size > 0) {
      // Filter aktivitas yang melibatkan pegawai tersebut, tanpa melihat timnya
      data = data.filter(a => a.users?.some(u => relevantPegawaiIds.has(u.id)));
    } else {
        // Jika tidak ada pegawai yang relevan, kembalikan array kosong
        data = [];
    }
  }

  // Default: Jika tidak ada mode filter yang cocok, kembalikan semua data
  return data;
});

const selectAllTeams = () => { selectedTeams.value = []; };
const toggleTeam = (team) => {
  const index = selectedTeams.value.findIndex(t => t.id === team.id);
  if (index > -1) { selectedTeams.value.splice(index, 1); }
  else { selectedTeams.value.push(team); }
};
const isTeamSelected = (team) => { return selectedTeams.value.some(t => t.id === team.id); };

const filteredPegawai = computed(() => {
  if (!searchQuery.value) {
    return allPegawai.value;
  }
  const query = searchQuery.value.toLowerCase();
  return allPegawai.value.filter(p => p.namaLengkap.toLowerCase().includes(query) || p.username.toLowerCase().includes(query));
});

const selectPegawai = (pegawai) => {
  selectedPegawaiId.value = pegawai.id;
  searchQuery.value = pegawai.id ? pegawai.namaLengkap : "";
  showDropdown.value = false;
};

const handleBlur = () => {
  setTimeout(() => { showDropdown.value = false; }, 200);
};

const daftarPegawaiTimeline = computed(() => {
  const pegawaiMap = new Map();

  // Jika ada tim yang dipilih, kumpulkan semua anggota dari tim tersebut
  if (mode.value === 'timeline' && selectedTeams.value.length > 0) {
    selectedTeams.value.forEach(t => {
      const teamData = teams.value.find(team => team.id === t.id);
      if (teamData && teamData.users) {
        teamData.users.forEach(u => pegawaiMap.set(u.id, u));
      }
    });
  } else {
    // Jika tidak ada tim yang dipilih, kumpulkan semua pegawai dari semua aktivitas yang ada
    aktivitas.value.forEach(a => {
      if (a.users) {
        a.users.forEach(u => pegawaiMap.set(u.id, u));
      }
    });
  }

  return Array.from(pegawaiMap.values()).sort((a, b) => a.namaLengkap.localeCompare(b.namaLengkap));
});

const calendarEvents = computed(() =>
  filteredActivities.value.map(a => {
    const endDate = a.tanggalSelesai ? new Date(a.tanggalSelesai) : new Date(a.tanggalMulai);
    endDate.setDate(endDate.getDate() + 1); // FullCalendar end date is exclusive
    
    return {
      id: a.id,
      title: a.namaAktivitas,
      start: a.tanggalMulai,
      end: endDate.toISOString().split('T')[0],
      backgroundColor: a.team?.warna || '#2563eb',
      borderColor: a.team?.warna || '#2563eb',
      textColor: '#fff'
    };
  })
);

const renderCalendar = () => {
  if (fullCalendarInstance) {
    fullCalendarInstance.destroy();
  }
  
  fullCalendarInstance = new Calendar(calendar.value, {
  plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
    initialView: "dayGridMonth",
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    initialView: "dayGridMonth",
    events: calendarEvents.value,
    locale: idLocale,
    buttonText: { 
      today: 'Hari Ini',
      month: 'Bulan',
      week: 'Minggu',
      day: 'Hari'
    },
    eventClick: (info) => {
      const id = info.event.id;
      router.push(`/aktivitas/detail/${id}`);
    },
    eventDidMount: (info) => {
      info.el.style.backgroundColor = info.event.extendedProps.backgroundColor;
      info.el.style.borderColor = info.event.extendedProps.borderColor;
      info.el.style.cursor = 'pointer';
      info.el.style.color = '#ffffff';
    }
  });
  fullCalendarInstance.render();
};

const timelineDates = computed(() => {
  const start = startOfMonth(timelineCurrentDate.value);
  const end = endOfMonth(timelineCurrentDate.value)
  const data = eachDayOfInterval({ start, end }).map(date => {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  });

  console.log("Start : ", start, " || End :  ", end, "|| Data : ", data);
  return data;
});

const getEventsForPegawai = (pegawaiId) => {
    const events = filteredActivities.value
        .filter(a => a.users && a.users.some(u => u.id === pegawaiId))
        .map(a => {
            const eventStart = a.tanggalMulai;
            const eventEnd = a.tanggalSelesai ? a.tanggalSelesai : a.tanggalMulai;
            
            return {
                ...a,
                title: a.namaAktivitas,
                start_time: a.jamMulai,
                end_time: a.jamSelesai,
                start: eventStart,
                end: eventEnd,
                backgroundColor: a.team?.warna || '#2563eb',
            };
        });

    const filteredByMonth = events.filter(e => {
        const eventStart = new Date(e.start);
        const eventEnd = e.end ? new Date(e.end) : eventStart;
        const currentMonthStart = startOfMonth(timelineCurrentDate.value);
        const currentMonthEnd = endOfMonth(timelineCurrentDate.value);

        return isWithinInterval(eventStart, { start: currentMonthStart, end: currentMonthEnd }) ||
               isWithinInterval(eventEnd, { start: currentMonthStart, end: currentMonthEnd }) ||
               (eventStart < currentMonthStart && eventEnd > currentMonthEnd);
    });
    
    return assignLanes(filteredByMonth);
};

const calculateEventWidth = (event) => {
  const eventStart = parseISO(event.start);
  const eventEnd = event.end ? parseISO(event.end) : eventStart;
  const currentMonthStart = startOfMonth(timelineCurrentDate.value);
  const currentMonthEnd = endOfMonth(timelineCurrentDate.value);
  const effectiveStart = eventStart < currentMonthStart ? currentMonthStart : eventStart;
  const effectiveEnd = eventEnd > currentMonthEnd ? currentMonthEnd : eventEnd;
  const days = differenceInDays(effectiveEnd, effectiveStart) + 1;
  return days * 50;
};

const calculateEventOffset = (event) => {
  const eventStart = parseISO(event.start);
  const currentMonthStart = startOfMonth(timelineCurrentDate.value);
  const effectiveStart = eventStart < currentMonthStart ? currentMonthStart : eventStart;
  const daysOffset = differenceInDays(effectiveStart, currentMonthStart);
  return daysOffset * 50;
};

const goToActivityDetail = (id) => {
  router.push(`/aktivitas/detail/${id}`);
};

onMounted(() => {
  fetchInitialData();
});

watch(mode, () => {
  // Reset filter saat mode berubah
  selectedTeams.value = [];
  selectedPegawaiId.value = null;

  // Jika mode baru adalah 'person', atur pegawai default ke kepala kantor
  if (mode.value === 'person') {
    const kepala = allPegawai.value.find(p => p.jabatan?.namaJabatan === "Kepala Kantor");
    if (kepala) {
      selectedPegawaiId.value = kepala.id;
    } else {
      selectedPegawaiId.value = allPegawai.value[0]?.id || null;
    }
  }

  fetchAktivitas();
});

watch([selectedTeams, selectedPegawaiId, mode], () => {
  fetchAktivitas();
});

watch(filteredActivities, (newActivities) => {
  if (mode.value === 'team' || mode.value === 'person') {
    nextTick(() => {
      renderCalendar();
    });
  }
});
</script>

<style scoped>
/* Style Timeline Custom yang disempurnakan */
.timeline-scroll-container {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.timeline-header-label-col, .timeline-row-label {
  flex-shrink: 0;
  width: 200px;
  max-width: 200px;
  line-height: 50px;
  white-space: nowrap;
  padding: 0 1rem;
  font-weight: 600;
  text-overflow: ellipsis;
  overflow: hidden;
  border-right: 1px solid #e5e7eb;
  background-color: #fff;
}
.dark .timeline-header-label-col, .dark .timeline-row-label {
  border-right-color: #4b5563;
  background-color: #1f2937;
  color: #e5e7eb;
}

.timeline-header-day-col {
  flex-shrink: 0;
  min-width: 50px;
  max-width: 50px;
  text-align: center;
  border-left: 1px solid #e5e7eb;
  border-bottom: 1px solid #e5e7eb;
  padding: 0.25rem 0.5rem;
  background-color: #fff;
}
.dark .timeline-header-day-col {
  border-left-color: #4b5563;
  border-bottom-color: #4b5563;
  background-color: #1f2937;
}

.bg-weekend-light {
  background-color: #f3f4f6; /* gray-100 */
}
.dark .bg-weekend-dark {
  background-color: #374151; /* gray-700 */
}

.timeline-row-wrap {
  display: flex;
  position: relative;
  height: auto;
}
.timeline-row-label {
  height: auto; /* Tinggi disesuaikan dengan konten */
  display: flex;
  align-items: center;
  position: sticky;
  left: 0;
  z-index: 1;
  padding: 0 1rem;
  border-bottom: 1px solid #e5e7eb;
}
.dark .timeline-row-label {
  border-bottom-color: #4b5563;
}

.timeline-row-content {
  flex-grow: 1;
  position: relative;
  min-height: 50px;
  border-left: 1px solid #e5e7eb;
}
.dark .timeline-row-content {
  border-left-color: #4b5563;
}
.timeline-row-label-container {
  flex-shrink: 0;
  min-width: 200px;
  max-width: 200px;
  position: sticky;
  left: 0;
  z-index: 2;
  background-color: #fff;
}
.dark .timeline-row-label-container {
  background-color: #1f2937;
}
.timeline-header-wrap {
  display: flex;
  flex-grow: 1;
}

.timeline-event-bar {
  position: absolute;
  height: 28px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  padding: 0 8px;
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  cursor: pointer;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out, filter 0.2s ease-in-out;
  z-index: 5;
}
.timeline-event-bar:hover {
  transform: scaleY(1.1);
  filter: brightness(1.2);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
  z-index: 6;
}
.event-title-text {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 10px;
  color: white;
}
.event-tooltip {
  position: absolute;
  bottom: calc(100% + 5px);
  left: 50%;
  transform: translateX(-50%);
  background-color: #333;
  color: white;
  padding: 6px 10px;
  border-radius: 6px;
  white-space: nowrap;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.2s ease-in-out;
  z-index: 10;
  display: flex;
  flex-direction: column;
}
.timeline-event-bar:hover .event-tooltip {
  opacity: 1;
  visibility: visible;
}
.fc-daygrid-event-harness {
  cursor: pointer;
}
.dark .fc-daygrid-day {
  background-color: #1f2937;
}
.dark .fc-daygrid-day-number {
  color: #e5e7eb;
}
.dark .fc-col-header-cell {
  background-color: #111827;
  color: #e5e7eb;
}
</style>