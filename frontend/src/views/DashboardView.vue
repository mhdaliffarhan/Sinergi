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
          <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Aktivitas Saya</h2>
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
          <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Aktivitas Saya</h2>
          <div ref="calendar" class="w-full"></div>
        </section>

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
import { isWithinInterval, startOfWeek, endOfWeek, compareAsc, isFuture, isToday, format, parseISO } from 'date-fns';
import { id } from 'date-fns/locale';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from "@fullcalendar/interaction";

import DashboardCard from '@/components/dashboard/DashboardCard.vue';
import DokumenProgressSection from '@/components/dashboard/DokumenProgressSection.vue';
import ModalAktivitas from '@/components/aktivitas/ModalAktivitas.vue';
import AktivitasCard from '@/components/aktivitas/AktivitasCard.vue';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

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
            const allAktivitasRes = await axios.get(`${baseURL}/api/aktivitas/kepala`);
            allAktivitasKepalaKantor.value = allAktivitasRes.data;
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
        return isFuture(tanggalMulai) || isFuture(tanggalSelesai) || isToday(tanggalMulai) || isToday(tanggalSelesai);
    }).sort((a, b) => {
        return compareAsc(new Date(a.tanggalMulai), new Date(b.tanggalMulai));
    });
};

const kalenderEventsData = computed(() => {
    if (isKepalaKantor.value) {
        return allAktivitasKepalaKantor.value;
    } else {
        return allAktivitas.value;
    }
});

const calendarEvents = computed(() =>
    kalenderEventsData.value.map(a => {
        const endDate = a.tanggalSelesai ? new Date(a.tanggalSelesai) : new Date(a.tanggalMulai);
        endDate.setDate(endDate.getDate() + 1);
        const isAllDay = !a.jamMulai && !a.jamSelesai;
        return {
            id: a.id,
            title: a.namaAktivitas,
            start: isAllDay ? a.tanggalMulai : `${a.tanggalMulai}T${a.jamMulai}`,
            end: isAllDay ? endDate.toISOString().split('T')[0] : `${a.tanggalSelesai || a.tanggalMulai}T${a.jamSelesai}`,
            allDay: isAllDay,
            backgroundColor: a.team?.warna || '#2563eb',
            borderColor: a.team?.warna || '#2563eb',
        };
    })
);

const renderCalendar = () => {
    if (!calendar.value) {
        console.error("Elemen kalender tidak ditemukan.");
        return;
    }
    if (fullCalendarInstance) {
        fullCalendarInstance.destroy();
    }
    fullCalendarInstance = new Calendar(calendar.value, {
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        initialView: isKepalaKantor.value || isKetuaTim.value ? 'timeGridWeek' : 'dayGridMonth',
        locale: idLocale,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        events: calendarEvents.value,
        buttonText: { 
            today: 'Hari Ini',
            month: 'Bulan',
            week: 'Minggu',
            day: 'Hari'
        },
        eventClick: (info) => {
            const id = info.event.id;
            openModal(id);
        },
        eventDidMount: (info) => {
        },
        slotMinTime: '07:00:00',
        slotMaxTime: '18:00:00',
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
.fc {
  /* Mengatur variabel warna global untuk FullCalendar */
  --fc-border-color: #e5e7eb; /* gray-200 */
  --fc-daygrid-event-dot-color: #ffffff; /* blue-600 */
  --fc-page-bg-color: #ffffff; /* white */
  --fc-neutral-bg-color: #f3f4f6; /* gray-100 */
  --fc-neutral-text-color: #6b7280; /* gray-500 */
}

/* Kustomisasi FullCalendar di Mode Gelap */
.dark .fc {
  --fc-border-color: #4b5563; /* gray-600 */
  --fc-daygrid-event-dot-color: #1f2937; /* blue-300 */
  --fc-page-bg-color: #1f2937; /* gray-800 */
  --fc-neutral-bg-color: #374151; /* gray-700 */
  --fc-neutral-text-color: #d1d5db; /* gray-400 */
}

/* Aturan umum untuk tampilan kalender */
.fc-daygrid-day,
.fc-timegrid-slot,
.fc-list-day {
  background-color: var(--fc-page-bg-color);
  color: var(--fc-neutral-text-color);
}

.fc-col-header-cell,
.fc-day-header {
  background-color: #f9fafb; /* gray-50 */
  color: #1f2937; /* gray-900 */
  border-color: var(--fc-border-color);
}

.dark .fc-col-header-cell,
.dark .fc-day-header {
  background-color: #111827; /* gray-900 */
  color: #e5e7eb; /* gray-200 */
}

/* Teks dan angka di kalender */
.fc-daygrid-day-number {
  color: #1f2937; /* gray-900 */
}

.dark .fc-daygrid-day-number {
  color: #e5e7eb; /* gray-200 */
}

/* Style untuk event/aktivitas */
.fc-event {
  color: #1f2937 !important; /* Teks hitam di mode terang */
  border-color: transparent !important; /* Menghilangkan border default */
}
.dark .fc-event {
  color: #ffffff !important; /* Teks putih di mode gelap */
}

/* Event yang seharian penuh */
.fc-daygrid-event {
  background-color: var(--fc-daygrid-event-dot-color);
  color: #ffffff; /* Teks putih untuk acara seharian */
}
.dark .fc-daygrid-event {
  color: #ffffff;
}
.fc-daygrid-event-harness {
  cursor: pointer;
}


/* Styling tombol FullCalendar */
.fc-button {
  background-color: #2563eb !important; /* Warna latar belakang biru */
  border-color: #2563eb !important; /* Warna border biru */
  color: #fff !important; /* Warna teks putih */
  box-shadow: none !important; /* Menghilangkan bayangan default */
}

/* Mengubah warna saat tombol dihover */
.fc-button:hover {
  background-color: #1d4ed8 !important; /* Warna biru lebih gelap saat dihover */
  border-color: #1d4ed8 !important;
}

/* Mengubah warna saat tombol ditekan (aktif) */
.fc-button:focus,
.fc-button:active {
  background-color: #1e40af !important; /* Warna biru lebih gelap lagi saat aktif */
  border-color: #1e40af !important;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.5) !important; /* Tambahkan ring fokus */
}

/* Aturan untuk mode gelap */
.dark .fc-button {
  background-color: #3b82f6 !important; /* Warna biru yang sedikit berbeda untuk dark mode */
  border-color: #3b82f6 !important;
  color: #fff !important;
}

.dark .fc-button:hover {
  background-color: #60a5fa !important;
  border-color: #60a5fa !important;
}

.dark .fc-button:focus,
.dark .fc-button:active {
  background-color: #3b82f6 !important;
  border-color: #3b82f6 !important;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5) !important;
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