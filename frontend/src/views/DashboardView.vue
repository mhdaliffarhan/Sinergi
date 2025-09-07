<template>
  <div class="container mx-auto p-4 sm:p-6 lg:p-8">
    <div v-if="isLoading" class="flex justify-center items-center h-64">
      <svg class="animate-spin -ml-1 mr-3 h-10 w-10 text-green-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
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
        <p class="mt-2 text-lg text-gray-600 dark:text-gray-300">Selamat datang, {{ authStore.user?.namaLengkap || 'Pengguna' }}!</p>
      </div>

      <div v-if="isKepalaKantor">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
          <DashboardCard icon="👥" title="Total Anggota" :value="totalAnggota" color="text-blue-500" />
          <DashboardCard icon="✅" title="Aktivitas Berjalan" :value="totalAktivitasKantor" color="text-orange-500" />
          <DashboardCard icon="💼" title="Proyek Berjalan" :value="totalProyekKantor" color="text-purple-500" />
          <DashboardCard icon="📅" title="Tim Aktif" :value="totalTimAktif" color="text-green-500" />
        </div>
        <section class="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6 mt-8">
          <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Jadwal Aktivitas Penting</h2>
          <div ref="calendar" class="w-full"></div>
        </section>
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
            Tidak ada kegiatan penting minggu ini.
          </div>
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
              :navigation="true"
              :breakpoints="{
                640: { slidesPerView: 2, spaceBetween: 20 },
                768: { slidesPerView: 3, spaceBetween: 30 },
                1024: { slidesPerView: 4, spaceBetween: 40 }
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

        <section class="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6 mt-8">
          <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-200">Progres Dokumen Wajib Saya</h2>
          <DokumenProgressSection 
            :dokumen-wajib="dokumenWajibSaya" 
            @go-to-aktivitas="goToAktivitas" 
          />
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
import { isWithinInterval, startOfWeek, endOfWeek, compareAsc } from 'date-fns';
import { Swiper, SwiperSlide } from 'swiper/vue';
import 'swiper/css';
import 'swiper/css/navigation';
import 'swiper/css/pagination';

import DashboardCard from '@/components/dashboard/DashboardCard.vue';
import DokumenProgressSection from '@/components/dashboard/DokumenProgressSection.vue';
import ModalAktivitas from '@/components/aktivitas/ModalAktivitas.vue';
import AktivitasCard from '@/components/aktivitas/AktivitasCard.vue';
import { format } from 'date-fns';

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

// Computed properties untuk Kepala Kantor
const totalAnggota = computed(() => allUsers.value.length);
const totalTimAktif = computed(() => allTeams.value.length);
const totalProyekKantor = computed(() => {
  const uniqueProjects = new Set();
  allAktivitas.value.forEach(a => a.project?.id && uniqueProjects.add(a.project.id));
  return uniqueProjects.size;
});
const totalAktivitasKantor = computed(() => allAktivitas.value.length);

// Computed properties untuk Ketua Tim
const teamMembers = computed(() => team.value?.users || []);
const teamProjects = computed(() => team.value?.projects || []);
const teamAktivitas = computed(() => {
  if (!selectedTeamId.value) return [];
  const selectedTeam = allTeams.value.find(t => t.id === selectedTeamId.value);
  return selectedTeam ? selectedTeam.aktivitas : [];
});

// Computed properties untuk Anggota Tim
const totalAktivitasSaya = computed(() => allAktivitas.value.length);
const dokumenBelumSelesai = computed(() => dokumenWajibSaya.value.filter(d => !d.statusPengecekan).length);
const aktivitasMingguIni = computed(() => {
  const today = new Date();
  const startOfThisWeek = startOfWeek(today, { weekStartsOn: 1 });
  const endOfThisWeek = endOfWeek(today, { weekStartsOn: 1 });

  return allAktivitas.value.filter(aktivitas => {
    // Tanggal mulai dan selesai dari aktivitas
    const tanggalMulai = new Date(aktivitas.tanggalMulai);
    const tanggalSelesai = aktivitas.tanggalSelesai ? new Date(aktivitas.tanggalSelesai) : tanggalMulai;

    console.log("Data || tanggal mulai : ", tanggalMulai, " || tanggal selesai : ", tanggalSelesai);
    // Periksa apakah ada irisan antara rentang aktivitas dengan rentang minggu ini
    const isOverlapping = (
      // Kasus 1: Aktivitas dimulai di dalam minggu ini
      isWithinInterval(tanggalMulai, { start: startOfThisWeek, end: endOfThisWeek }) ||
      // Kasus 2: Aktivitas berakhir di dalam minggu ini
      isWithinInterval(tanggalSelesai, { start: startOfThisWeek, end: endOfThisWeek }) ||
      // Kasus 3: Aktivitas dimulai sebelum dan berakhir setelah minggu ini
      (tanggalMulai < startOfThisWeek && tanggalSelesai > endOfThisWeek)
    );

    return isOverlapping;
  }).length;
});

// Pengurutan aktivitas anggota tim berdasarkan progres dokumen
const sortedAktivitasSaya = computed(() => {
  return [...allAktivitas.value].sort((a, b) => {
    const aProgress = a.daftarDokumenWajib?.filter(doc => doc.dokumenId !== null).length ?? 0;
    const bProgress = b.daftarDokumenWajib?.filter(doc => doc.dokumenId !== null).length ?? 0;
    const aTotal = a.daftarDokumenWajib?.length ?? 0;
    const bTotal = b.daftarDokumenWajib?.length ?? 0;

    const aCompletion = aTotal > 0 ? aProgress / aTotal : 1;
    const bCompletion = bTotal > 0 ? bProgress / bTotal : 1;
    
    // Urutkan dari yang progresnya paling rendah ke tertinggi
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

    if (isKepalaKantor.value) {
      const [aktivitasRes, teamsRes, usersRes, aktivitasKepalaRes] = await Promise.all([
        axios.get('http://127.0.0.1:8000/api/kalender/events'),
        axios.get('http://127.0.0.1:8000/api/teams/active'),
        axios.get('http://127.0.0.1:8000/api/users', { params: { limit: 10000 } }),
        axios.get('http://127.0.0.1:8000/api/aktivitas/penting')
      ]);
      allAktivitas.value = aktivitasRes.data;
      allTeams.value = teamsRes.data;
      allUsers.value = usersRes.data.items;
      upcomingAktivitasKantor.value = aktivitasKepalaRes.data;
      renderCalendar(upcomingAktivitasKantor.value);

    } else if (isKetuaTim.value) {
      const teamId = selectedTeamId.value;
      if (teamId) {
        const [aktivitasRes, teamDetailsRes, dokumenRes] = await Promise.all([
          axios.get(`http://127.0.0.1:8000/api/kalender/events?team_ids=${teamId}`),
          axios.get(`http://127.0.0.1:8000/api/teams/${teamId}/details`),
          axios.get(`http://127.0.0.1:8000/api/teams/${teamId}/dokumen-wajib-team`)
        ]);
        allAktivitas.value = aktivitasRes.data;
        team.value = teamDetailsRes.data;
        dokumenWajibTeam.value = dokumenRes.data;
        renderCalendar(allAktivitas.value);
      }
    } else { // Anggota Tim
      const [aktivitasRes, dokumenRes] = await Promise.all([
        axios.get(`http://127.0.0.1:8000/api/users/${user.id}/aktivitas`),
        axios.get(`http://127.0.0.1:8000/api/users/${user.id}/dokumen-wajib`)
      ]);
      allAktivitas.value = aktivitasRes.data;
      dokumenWajibSaya.value = dokumenRes.data;
      renderCalendar(allAktivitas.value);
    }
  } catch (error) {
    toast.error('Gagal memuat data dashboard.');
    console.error('Error fetching dashboard data:', error);
  } finally {
    isLoading.value = false;
  }
};

const renderCalendar = (eventsData) => {
  if (!calendar.value) {
    console.error("Elemen kalender tidak ditemukan.");
    return;
  }

  if (fullCalendarInstance) {
    fullCalendarInstance.destroy();
  }
  
  const events = eventsData.map(aktivitas => ({
    title: aktivitas.namaAktivitas,
    start: aktivitas.tanggalMulai,
    end: aktivitas.tanggalSelesai ? new Date(new Date(aktivitas.tanggalSelesai).setDate(new Date(aktivitas.tanggalSelesai).getDate() + 1)) : aktivitas.tanggalMulai,
    extendedProps: {
      aktivitasId: aktivitas.id,
      teamColor: aktivitas.team?.warna || '#3b82f6'
    }
  }));

  fullCalendarInstance = new Calendar(calendar.value, {
    plugins: [dayGridPlugin],
    initialView: 'dayGridMonth',
    locale: idLocale,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,dayGridWeek'
    },
    events: events,
    eventDidMount: (info) => {
      info.el.style.backgroundColor = info.event.extendedProps.teamColor;
      info.el.style.borderColor = info.event.extendedProps.teamColor;
      info.el.style.cursor = 'pointer';
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
    const response = await axios.get(`http://127.0.0.1:8000/api/aktivitas/${aktivitasId}`);
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
  const options = { day: 'numeric', month: 'short', year: 'numeric' };
  const startDate = new Date(start);
  const endDate = end ? new Date(end) : null;
  if (endDate) {
    return `${format(startDate, 'd MMMM yyyy', { locale: id })} - ${format(endDate, 'd MMMM yyyy', { locale: id })}`;
  }
  return format(startDate, 'd MMMM yyyy', { locale: id });
};

// Logika untuk dropdwon Ketua Tim
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

watch(allAktivitas, (newAktivitas) => {
    if (newAktivitas) {
        nextTick(() => {
            renderCalendar(newAktivitas);
        });
    }
});

onMounted(() => {
  watch(() => authStore.user, (newUser) => {
    if (newUser) {
      fetchDashboardData();
    }
  }, { immediate: true });
});
</script>