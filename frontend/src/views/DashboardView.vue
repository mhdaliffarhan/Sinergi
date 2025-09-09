<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <svg class="animate-spin -ml-1 mr-3 h-10 w-10 text-green-500" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </div>

    <div v-else-if="!authStore.user" class="text-center text-gray-500 dark:text-gray-400 py-10">
      Silakan login untuk melihat dashboard.
    </div>

    <div v-else class="space-y-8">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Dashboard {{ dashboardTitle }}</h1>
      </div>

      <div v-if="isKepalaKantor">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 gap-6 mt-6">
          <DashboardCard icon="👥" title="Total Pegawai" :value="totalAnggota" color="text-blue-500" />
          <!-- <DashboardCard icon="💼" title="Proyek Aktif" :value="totalProyekKantor" color="text-purple-500" />
          <DashboardCard icon="✅" title="Aktivitas Berjalan" :value="totalAktivitasKantor" color="text-orange-500" /> -->
          <DashboardCard icon="📅" title="Tim Aktif" :value="totalTimAktif" color="text-green-500" />
        </div>
        
        <section class="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6 mt-8">
          <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Kegiatan Minggu Ini</h2>
          <div v-if="upcomingAktivitasKantor.length > 0" class="divide-y divide-gray-200 dark:divide-gray-700">
            <div v-for="aktivitas in upcomingAktivitasKantor" :key="aktivitas.id" class="flex items-center gap-4 py-3">
              <span class="text-xl">🗓️</span>
              <div class="flex-grow">
                <router-link :to="{ name: 'aktivitas-detail', params: { id: aktivitas.id } }" class="text-gray-900 dark:text-white font-medium hover:underline">
                  {{ aktivitas.namaAktivitas }}
                </router-link>
                <p class="text-sm text-gray-500 dark:text-gray-400">
                  {{ formatPeriode(aktivitas.tanggalMulai, aktivitas.tanggalSelesai) }}
                </p>
              </div>
              <span class="text-xs font-medium px-2 py-1 rounded-full text-white" :style="{ backgroundColor: aktivitas.team?.warna || '#3b82f6' }">
                {{ aktivitas.team?.namaTim || '-' }}
              </span>
            </div>
          </div>
          <div v-else class="text-center text-gray-500 dark:text-gray-400 p-6">
            Tidak ada kegiatan minggu ini.
          </div>
        </section>
        
        <section class="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6 mt-8">
          <div class="flex items-center gap-4 mb-4 flex-wrap">
            <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200">Aktivitas Saya</h2>
          </div>
          <div ref="calendar" class="w-full"></div>
        </section>
      </div>

      <div v-else-if="isKetuaTim">
        <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-6 gap-4">
          <div class="flex items-center gap-3 w-full sm:w-auto">
            <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-200 whitespace-nowrap">Tim Yang Dipantau:</h2>
            <select v-model="selectedTeamId" class="w-full sm:w-64 px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm dark:bg-gray-700 dark:text-white focus:outline-none focus:ring-blue-500 focus:border-blue-500">
              <option v-for="team in authStore.user?.ketuaTimAktif" :key="team.id" :value="team.id">
                {{ team.namaTim }}
              </option>
            </select>
          </div>
          <div class="flex-grow"></div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mt-6">
          <DashboardCard icon="👥" title="Anggota Tim" :value="teamMembers?.length ?? 0" color="text-blue-500" />
          <DashboardCard icon="💼" title="Proyek Tim" :value="teamProjects?.length ?? 0" color="text-purple-500" />
          <DashboardCard icon="✅" title="Aktivitas Tim" :value="teamAktivitas?.length ?? 0" color="text-orange-500" />
        </div>

        <section class="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6 mt-8">
          <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Progress Dokumen Tim</h2>
          <DokumenProgressSection v-if="dokumenWajibTeam.length > 0" :dokumen-wajib="dokumenWajibTeam" @go-to-aktivitas="goToAktivitas" />
          <div v-else class="text-center text-gray-500 dark:text-gray-400 p-6">
            Tim ini tidak memiliki dokumen wajib yang harus diselesaikan.
          </div>
        </section>

        <section class="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6 mt-8">
          <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Jadwal Anggota Tim Saya</h2>
          <div ref="calendar" class="w-full"></div>
        </section>
      </div>

      <div v-else>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6 mt-6">
          <DashboardCard icon="📝" title="Aktivitas Saya" :value="totalAktivitasSaya" color="text-blue-500" />
          <DashboardCard icon="🗓️" title="Aktivitas Minggu Ini" :value="aktivitasMingguIni" color="text-green-500" />
          <DashboardCard icon="⏳" title="Dokumen Belum Selesai" :value="dokumenBelumSelesai" color="text-red-500" />
        </div>
        
        <section class="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6 mt-8">
          <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Aktivitas Berjalan Saya</h2>
          <div v-if="sortedAktivitasSaya.length > 0">
            <swiper
              :slides-per-view="1"
              :space-between="16"
              :pagination="{ clickable: true }"
              :breakpoints="{
                
                510: { slidesPerView: 1, spaceBetween: 20 },
                640: { slidesPerView: 2, spaceBetween: 20 },
                1115: { slidesPerView: 3, spaceBetween: 20 },
                1300: { slidesPerView: 4, spaceBetween: 20 }
              }"
              class="my-swiper"
            >
              <swiper-slide v-for="aktivitas in sortedAktivitasSaya" :key="aktivitas.id">
                <AktivitasCard :aktivitas="aktivitas" :is-dashboard="true"/>
              </swiper-slide>
            </swiper>
          </div>
          <div v-else class="text-center text-gray-500 dark:text-gray-400 p-6">
            Tidak ada aktivitas yang sedang berjalan untuk Anda.
          </div>
        </section>

        <section class="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6 mt-8">
          <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Jadwal Aktivitas Saya</h2>
          <div ref="calendar" class="w-full"></div>
        </section>

        <!-- <section class="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6 mt-8">
          <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Progres Dokumen Wajib Saya</h2>
          <DokumenProgressSection 
            :dokumen-wajib="dokumenWajibSaya" 
            @go-to-aktivitas="goToAktivitas" 
          />
        </section> -->
      </div>
    </div>
  </div>
  <ModalAktivitas v-if="isModalOpen" :aktivitas="selectedAktivitas" @close="closeModal" @go-to-detail="goToAktivitas" />
</template>

<script setup>
import { ref, onMounted, computed, watch, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { useToast } from 'vue-toastification';
import { Calendar } from '@fullcalendar/core';
import dayGridPlugin from '@fullcalendar/daygrid';
import idLocale from '@fullcalendar/core/locales/id';
import { isWithinInterval, startOfWeek, endOfWeek, compareAsc, isFuture, isToday } from 'date-fns';
import { id } from 'date-fns/locale';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

import DashboardCard from '@/components/dashboard/DashboardCard.vue';
import DokumenProgressSection from '@/components/dashboard/DokumenProgressSection.vue';
import ModalAktivitas from '@/components/aktivitas/ModalAktivitas.vue';
import AktivitasCard from '@/components/aktivitas/AktivitasCard.vue';
import { format } from 'date-fns';
import timeGridPlugin from '@fullcalendar/timegrid';
import ModalWrapper from '@/components/ModalWrapper.vue';

const baseURL = import.meta.env.VITE_API_BASE_URL;
const authStore = useAuthStore();
const router = useRouter();
const toast = useToast();

const isLoading = ref(true);
const calendar = ref(null);
let fullCalendarInstance = null;

const allAktivitas = ref([]);
const allTeams = ref([]);
const allUsers = ref([]);
const team = ref(null);
const dokumenWajibSaya = ref([]);
const dokumenWajibTeam = ref([]);
const selectedTeamId = ref(null);
const upcomingAktivitasKantor = ref([]);
const calendarFilter = ref('saya');
const allAktivitasKepalaKantor = ref([]);


const isModalOpen = ref(false);
const selectedAktivitas = ref(null);

const isKepalaKantor = computed(() => authStore.user?.jabatan?.namaJabatan === 'Kepala Kantor');
const isKetuaTim = computed(() => authStore.user?.isKetuaTim === true);
const isAnggotaTim = computed(() => !isKepalaKantor.value && !isKetuaTim.value);

const dashboardTitle = computed(() => {
  if (isKepalaKantor.value) return 'Kantor';
  if (isKetuaTim.value) return 'Tim Saya';
  return 'Saya';
});

const totalAnggota = computed(() => allUsers.value.length);
const totalTimAktif = computed(() => allTeams.value.length);
const totalProyekKantor = computed(() => {
  const uniqueProjects = new Set();
  allAktivitas.value.forEach(a => a.project?.id && uniqueProjects.add(a.project.id));
  return uniqueProjects.size;
});
const totalAktivitasKantor = computed(() => allAktivitas.value.length);

const teamMembers = computed(() => team.value?.users || []);
const teamProjects = computed(() => team.value?.projects || []);
const teamAktivitas = computed(() => {
  if (!selectedTeamId.value) return [];
  const selectedTeam = allTeams.value.find(t => t.id === selectedTeamId.value);
  return selectedTeam ? selectedTeam.aktivitas : [];
});

const totalAktivitasSaya = computed(() => allAktivitas.value.length);
const dokumenBelumSelesai = computed(() => dokumenWajibSaya.value.filter(d => !d.statusPengecekan).length);
const aktivitasMingguIni = computed(() => {
  const today = new Date();
  const startOfThisWeek = startOfWeek(today, { weekStartsOn: 1 });
  const endOfThisWeek = endOfWeek(today, { weekStartsOn: 1 });
  return allAktivitas.value.filter(aktivitas => {
    const tanggalMulai = new Date(aktivitas.tanggalMulai);
    const tanggalSelesai = aktivitas.tanggalSelesai ? new Date(aktivitas.tanggalSelesai) : tanggalMulai;
    const isOverlapping = (
      isWithinInterval(tanggalMulai, { start: startOfThisWeek, end: endOfThisWeek }) ||
      isWithinInterval(tanggalSelesai, { start: startOfThisWeek, end: endOfThisWeek }) ||
      (tanggalMulai < startOfThisWeek && tanggalSelesai > endOfThisWeek)
    );
    return isOverlapping;
  }).length;
});

const sortedAktivitasSaya = computed(() => {
  return [...allAktivitas.value].sort((a, b) => {
    const aProgress = a.daftarDokumenWajib?.filter(doc => doc.dokumenId !== null).length ?? 0;
    const bProgress = b.daftarDokumenWajib?.filter(doc => doc.dokumenId !== null).length ?? 0;
    const aTotal = a.daftarDokumenWajib?.length ?? 0;
    const bTotal = b.daftarDokumenWajib?.length ?? 0;

    const aCompletion = aTotal > 0 ? aProgress / aTotal : 1;
    const bCompletion = bTotal > 0 ? bProgress / bTotal : 1;
    
    return aCompletion - bCompletion;
  });
});

const fetchDashboardData = async () => {
  isLoading.value = true;
  try {
    const user = authStore.user;
    if (!user) {
      router.push({ name: 'login' });
      return;
    }
    
    const [teamsRes, usersRes] = await Promise.all([
      axios.get(`${baseURL}/api/teams/active`),
      axios.get(`${baseURL}/api/users`, { params: { limit: 10000 } })
    ]);
    allTeams.value = teamsRes.data;
    allUsers.value = usersRes.data.items;

    if (isKepalaKantor.value) {
      // Ambil semua data aktivitas dari endpoint kepala kantor
      const allAktivitasRes = await axios.get(`${baseURL}/api/aktivitas/kepala`);

      // Simpan semua aktivitas kantor
      allAktivitasKepalaKantor.value = allAktivitasRes.data;

      // Filter aktivitas yang akan datang dari data yang sama
      filterUpcomingAktivitas();

    } else if (isKetuaTim.value) {
      const teamId = selectedTeamId.value;
      if (teamId) {
        const [aktivitasRes, teamDetailsRes, dokumenRes] = await Promise.all([
          axios.get(`${baseURL}/api/kalender/events?team_ids=${teamId}`),
          axios.get(`${baseURL}/api/teams/${teamId}/details`),
          axios.get(`${baseURL}/api/teams/${teamId}/dokumen-wajib-team`)
        ]);
        allAktivitas.value = aktivitasRes.data;
        team.value = teamDetailsRes.data;
        dokumenWajibTeam.value = dokumenRes.data;
      }
    } else { // Anggota Tim
      const [aktivitasRes, dokumenRes] = await Promise.all([
        axios.get(`${baseURL}/api/users/${user.id}/aktivitas`),
        axios.get(`${baseURL}/api/users/${user.id}/dokumen-wajib`)
      ]);
      allAktivitas.value = aktivitasRes.data;
      dokumenWajibSaya.value = dokumenRes.data;
    }

  } catch (error) {
    toast.error('Gagal memuat data dashboard.');
    console.error('Error fetching dashboard data:', error);
  } finally {
    isLoading.value = false;
  }
};

const filterUpcomingAktivitas = () => {
  const today = new Date();
  upcomingAktivitasKantor.value = allAktivitasKepalaKantor.value.filter(aktivitas => {
    const tanggalMulai = new Date(aktivitas.tanggalMulai);
    const tanggalSelesai = aktivitas.tanggalSelesai ? new Date(aktivitas.tanggalSelesai) : tanggalMulai;

    // Cek apakah tanggal mulai atau tanggal selesai berada di masa depan atau hari ini
    return isFuture(tanggalMulai) || isFuture(tanggalSelesai) || isToday(tanggalMulai) || isToday(tanggalSelesai);
  }).sort((a, b) => {
    // Urutkan berdasarkan tanggal mulai terdekat
    return compareAsc(new Date(a.tanggalMulai), new Date(b.tanggalMulai));
  });
};

const renderCalendar = () => {
  if (!calendar.value) {
    console.error("Elemen kalender tidak ditemukan.");
    return;
  }

  if (fullCalendarInstance) {
    fullCalendarInstance.destroy();
  }
  
  const events = kalenderEventsData.value.map(aktivitas => ({
    title: aktivitas.namaAktivitas,
    start: aktivitas.tanggalMulai,
    end: aktivitas.tanggalSelesai ? new Date(new Date(aktivitas.tanggalSelesai).setDate(new Date(aktivitas.tanggalSelesai).getDate() + 1)) : aktivitas.tanggalMulai,
    extendedProps: {
      aktivitasId: aktivitas.id,
      teamColor: aktivitas.team?.warna || '#3b82f6'
    }
  }));

  fullCalendarInstance = new Calendar(calendar.value, {
    plugins: [dayGridPlugin, timeGridPlugin],
    initialView: isKepalaKantor.value ? 'dayGridWeek' : 'dayGridMonth',
    locale: idLocale,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,dayGridWeek,dayGridDay'
    },
    events: events,
    eventDidMount: (info) => {
      info.el.style.backgroundColor = info.event.extendedProps.teamColor;
      info.el.style.borderColor = info.event.extendedProps.teamColor;
      info.el.style.cursor = 'pointer';
      info.el.style.color = '#ffffff';
    },
    eventClick: (info) => {
      const aktivitasId = info.event.extendedProps.aktivitasId;
      openModal(aktivitasId);
    }
  });
  fullCalendarInstance.render();
};

const openModal = async (aktivitasId) => {
  try {
    const response = await axios.get(`${baseURL}/api/aktivitas/${aktivitasId}`);
    selectedAktivitas.value = response.data;
    isModalOpen.value = true;
  } catch (error) {
    toast.error('Gagal memuat detail aktivitas.');
    console.error('Error fetching aktivitas details:', error);
  }
};

const closeModal = () => {
  isModalOpen.value = false;
  selectedAktivitas.value = null;
};

const goToAktivitas = (id) => {
  router.push({ name: 'aktivitas-detail', params: { id: id } });
};

const formatPeriode = (start, end) => {
    if (!start) return '-';
    const startDate = new Date(start);
    const endDate = end ? new Date(end) : null;
    if (endDate) {
        return `${format(startDate, 'd MMMM yyyy', { locale: id })} - ${format(endDate, 'd MMMM yyyy', { locale: id })}`;
    }
    return format(startDate, 'd MMMM yyyy', { locale: id });
};

const kalenderEventsData = computed(() => {
    if (isKepalaKantor.value) {
        return allAktivitasKepalaKantor.value;
    } else {
        return allAktivitas.value;
    }
});

watch(() => authStore.user?.ketuaTimAktif, (newVal) => {
  if (newVal && newVal.length > 0) {
    selectedTeamId.value = newVal[0].id;
  }
}, { immediate: true });

watch(selectedTeamId, () => {
  if (isKetuaTim.value) {
    fetchDashboardData();
  }
});

watch(calendarFilter, () => {
    if (isKepalaKantor.value) {
        nextTick(() => {
            renderCalendar();
        });
    }
});

watch(allAktivitas, () => {
    nextTick(() => {
        renderCalendar();
    });
});

watch(allAktivitasKepalaKantor, () => {
    filterUpcomingAktivitas();
    nextTick(() => {
        renderCalendar();
    });
});

onMounted(() => {
  watch(() => authStore.user, (newUser) => {
    if (newUser) {
      fetchDashboardData();
    }
  }, { immediate: true });
});
</script>

<style>
/* Style kalender */
.fc-toolbar.fc-header-toolbar {
  margin-bottom: 1.5rem;
}
.fc-toolbar-title {
  font-size: 1.5rem;
  font-weight: 700;
}
.dark .fc-toolbar-title,
.dark .fc-button-primary {
  color: #fff;
}
.dark .fc-button-primary:hover {
  color: #eee;
}
.dark .fc-daygrid-day-number,
.dark .fc-col-header-cell-cushion {
  color: #ccc;
}
.dark .fc-day-other .fc-daygrid-day-number {
  color: #6b7280;
}
.dark .fc-daygrid-day {
  background-color: #1f2937;
  border-color: #4b5563;
}
.dark .fc-day-today {
  background-color: #2e3a47 !important;
}
.dark .fc-day-today .fc-daygrid-day-number {
  color: #fff;
}
.dark .fc-daygrid-event {
  color: #fff;
}
.dark .fc-theme-standard .fc-scrollgrid {
  border-color: #4b5563;
}
.dark .fc-theme-standard td,
.dark .fc-theme-standard th {
  border-color: #4b5563;
}

/* Style timeline */
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
  background-color: #f3f4f6;
}
.dark .bg-weekend-dark {
  background-color: #374151;
}
.timeline-row-wrap {
  display: flex;
  position: relative;
  height: auto;
}
.timeline-row-label {
  height: auto;
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
  color: white;
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