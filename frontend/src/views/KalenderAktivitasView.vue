<template>
  <div class="space-y-6">
    <div class=" bg-white dark:bg-gray-800 shadow-md rounded-xl p-4 transition hover:shadow-lg">
      <div class="flex flex-col gap-6">
        
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
            <label class="font-semibold text-gray-700 dark:text-gray-200">Rentang Tanggal:</label>
            <input
              type="date"
              v-model="dateRange.start"
              class="border rounded-lg px-2 py-1 dark:bg-gray-700 dark:text-gray-100 dark:border-gray-600"
            />
            <span class="dark:text-gray-200">-</span>
            <input
              type="date"
              v-model="dateRange.end"
              class="border rounded-lg px-2 py-1 dark:bg-gray-700 dark:text-gray-100 dark:border-gray-600"
            />
          </div>
        </div>

        <div class="flex flex-col sm:flex-row sm:items-start gap-3">
          
          <div class="flex flex-wrap gap-2">
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
        </div>
      </div>
    </div>

    <div v-if="mode === 'calendar'" class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow">
      <FullCalendar :options="calendarOptions" />
    </div>

    <div v-else class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow">
      <Timeline :events="timelineEvents" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from 'vue-router';
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import idLocale from '@fullcalendar/core/locales/id'; 
import axios from "axios";
import Timeline from "@/components/Timeline.vue";
import { useToast } from 'vue-toastification';

const apiUrl = import.meta.env.VITE_API_BASE_URL;
const toast = useToast();
const router = useRouter();
const mode = ref("calendar");
const selectedTeams = ref([]); // Tetap array, tapi sekarang untuk menyimpan objek tim yang dipilih
const teams = ref([]);
const dateRange = ref({ start: "", end: "" });
const aktivitas = ref([]);

// 🔹 Ambil data tim & aktivitas dari backend (Tidak ada perubahan)
onMounted(async () => {
  try {
    const [aktivitasResponse, teamsResponse] = await Promise.all([
      axios.get(`${apiUrl}/api/aktivitas`),
      axios.get(`${apiUrl}/api/teams?limit=1000`)
    ]);
    aktivitas.value = aktivitasResponse.data;
    teams.value = teamsResponse.data.items;
  } catch (err) {
    console.error("Gagal mengambil data awal:", err);
    toast.error("Gagal mengambil data Aktivitas");
  }
});

// filtering (Tidak ada perubahan, logika ini sudah mendukung sistem baru)
const filteredActivities = computed(() => {
  let data = aktivitas.value;

  // Jika ada tim yang dipilih, filter berdasarkan ID tim tersebut
  if (selectedTeams.value.length > 0) {
    const teamIds = selectedTeams.value.map(t => t.id);
    data = data.filter(a => a.team && teamIds.includes(a.team.id));
  }
  // Jika tidak ada tim yang dipilih (panjang array 0), filter ini dilewati, menampilkan semua.

  if (mode.value === "timeline" && dateRange.value.start && dateRange.value.end) {
    const startFilter = new Date(dateRange.value.start);
    const endFilter = new Date(dateRange.value.end);
    endFilter.setHours(23, 59, 59, 999);
    data = data.filter(a => {
      if (!a.tanggalMulai) return false;
      const eventStart = new Date(a.tanggalMulai);
      const eventEnd = a.tanggalSelesai ? new Date(a.tanggalSelesai) : eventStart;
      return eventEnd >= startFilter && eventStart <= endFilter;
    });
  }

  return data;
});

const selectAllTeams = () => {
  selectedTeams.value = [];
};

const toggleTeam = (team) => {
  const index = selectedTeams.value.findIndex(t => t.id === team.id);
  if (index > -1) {
    // Jika tim sudah ada di array, hapus (unselect)
    selectedTeams.value.splice(index, 1);
  } else {
    // Jika tim belum ada, tambahkan (select)
    selectedTeams.value.push(team);
  }
};

const isTeamSelected = (team) => {
  return selectedTeams.value.some(t => t.id === team.id);
};

// --- Logika Kalender dan Timeline (Tidak ada perubahan signifikan) ---

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
  buttonText: {
    today: 'Hari Ini', // Mengganti teks 'today'
  },
}));

const timelineEvents = computed(() =>
  filteredActivities.value.map(a => ({
    id: a.id,
    title: a.namaAktivitas,
    description: a.deskripsi,
    date: a.tanggalSelesai ? `${a.tanggalMulai} s.d. ${a.tanggalSelesai}` : a.tanggalMulai,
    status: a.daftarDokumenWajib?.some(d => d.status === "Wajib Diunggah")
      ? "Belum Lengkap"
      : "Lengkap",
    team: a.team 
  }))
);
</script>

<style>
/* Membuat event di kalender menjadi interaktif saat di-hover */
.fc-daygrid-event:hover {
  cursor: pointer;
  transform: scale(1.02);
  transition: transform 0.2s ease-in-out;
  filter: brightness(1.1);
}

/* Menyesuaikan warna tombol utama (Prev, Next, Hari Ini) dengan tema */
.fc .fc-button-primary {
  background-color: #2563eb; /* Sesuai dengan bg-blue-600 */
  border-color: #2563eb;
  transition: background-color 0.2s;
}

/* Warna tombol saat di-hover */
.fc .fc-button-primary:hover {
  background-color: #1d4ed8; /* Sesuai dengan bg-blue-700 */
  border-color: #1d4ed8;
}

/* Warna tombol saat aktif/diklik */
.fc .fc-button-primary:active {
  background-color: #1e40af !important; /* Sesuai dengan bg-blue-800 */
  border-color: #1e40af !important;
}

/* Menghapus fokus outline yang kurang menarik */
.fc .fc-button-primary:focus {
  box-shadow: none;
}

.dark .fc .fc-col-header-cell-cushion, /* Nama hari (Sen, Sel, ...) */
.dark .fc .fc-daygrid-day-number,    /* Nomor tanggal (1, 2, 3, ...) */
.dark .fc .fc-toolbar-title,         /* Judul bulan (Agustus 2025) */
.dark .fc a:not(.fc-event) {         /* Teks lain yang berupa link */
  color: #e5e7eb; /* gray-200, warna putih keabuan yang nyaman di mata */
}

/* Teks event di dark mode dibuat putih agar kontras dengan warna background event */
.dark .fc-daygrid-event .fc-event-title {
  color: #ffffff;
}
</style>