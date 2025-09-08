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
      </div>
    </div>

    <div v-if="mode === 'calendar'" class="bg-white dark:bg-gray-800 rounded-xl p-4 shadow">
      <FullCalendar :options="calendarOptions" />
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

const baseURL = import.meta.env.VITE_API_BASE_URL;
const toast = useToast();
const router = useRouter();

const mode = ref("calendar");
const selectedPegawaiId = ref("");
const aktivitas = ref([]);
const allPegawai = ref([]);
const searchQuery = ref("");
const showDropdown = ref(false);

onMounted(async () => {
  try {
    const [aktivitasResponse, pegawaiResponse] = await Promise.all([
      axios.get(`${baseURL}/api/aktivitas`),
      axios.get(`${baseURL}/api/users?limit=1000`)
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

</script>