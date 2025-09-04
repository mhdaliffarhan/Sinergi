<template>
  <div class="overflow-x-auto">
    <div class="relative w-full pb-8 min-w-[768px]">
      
      <div class="grid grid-cols-12 gap-x-1 font-semibold text-xs text-center text-gray-500 dark:text-gray-400 border-b dark:border-gray-700">
        <div class="col-span-2 py-2 text-left px-2">Aktivitas</div>
        <div class="col-span-10 flex border-l dark:border-gray-700">
          <div v-for="day in daysInDateRange" :key="day.toISOString()" class="flex-1 py-2 border-r dark:border-gray-700">
            {{ format(day, 'EEE') }} <br />
            <span class="text-xs font-normal">{{ format(day, 'dd') }}</span> </div>
        </div>
      </div>
      
      <div v-if="events.length > 0" class="flex flex-col">
        <div v-for="event in events" :key="event.id" class="grid grid-cols-12 gap-x-1 py-4 border-b dark:border-gray-700 relative">
          <div class="col-span-2 px-2 text-sm font-medium text-gray-900 dark:text-gray-200 truncate">
            <span class="inline-flex items-center px-2 py-1 text-xs font-medium rounded-full text-white"
              :style="{ backgroundColor: event.team?.warna || '#2563eb' }">
              {{ event.team?.namaTim || 'Tanpa Tim' }}
            </span>
            <div class="mt-1 font-normal">{{ event.title }}</div>
          </div>
          <div class="col-span-10 relative border-l dark:border-gray-700">
            <div v-for="(day, index) in daysInDateRange" :key="index" class="absolute h-full top-0 border-l border-gray-100 dark:border-gray-700" :style="{ left: `${(index / daysInDateRange.length) * 100}%` }"></div>
            <div
              class="absolute h-8 rounded-lg shadow-sm top-1/2 -translate-y-1/2 flex items-center px-2 transition-all duration-300 ease-in-out cursor-pointer hover:scale-105"
              :style="{
                backgroundColor: event.team?.warna || '#2563eb',
                left: `${getEventPosition(event).left}%`,
                width: `${getEventPosition(event).width}%`
              }"
              :title="`${event.title} (${event.date})`"
              @click="goToDetail(event.id)"
            >
              <span class="text-white text-xs font-semibold whitespace-nowrap overflow-hidden">
                {{ event.title }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-center py-8 text-gray-500 dark:text-gray-400">
        Tidak ada aktivitas pada rentang tanggal ini.
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { format, eachDayOfInterval, parseISO, differenceInDays } from 'date-fns';
import { id } from 'date-fns/locale';
import { useRouter } from 'vue-router';

const props = defineProps({
  events: {
    type: Array,
    required: true,
  },
  dateRange: {
    type: Object,
    required: true,
  },
});

const router = useRouter();

// Menghitung jumlah hari dalam rentang tanggal
const daysInDateRange = computed(() => {
  if (!props.dateRange.start || !props.dateRange.end) return [];
  const start = parseISO(props.dateRange.start);
  const end = parseISO(props.dateRange.end);
  return eachDayOfInterval({ start, end });
});

// Menghitung posisi dan lebar bar timeline
const getEventPosition = (event) => {
  if (!props.dateRange.start || !props.dateRange.end) return { left: 0, width: 0 };
  
  const rangeStart = parseISO(props.dateRange.start);
  const eventStart = parseISO(event.start);
  const eventEnd = event.end ? parseISO(event.end) : eventStart;
  
  // Hitung total durasi rentang tanggal yang ditampilkan (dalam hari)
  const totalDays = differenceInDays(parseISO(props.dateRange.end), rangeStart) + 1;
  
  // Hitung offset dari awal rentang (dalam hari)
  const daysFromStart = differenceInDays(eventStart, rangeStart);
  
  // Hitung durasi event (dalam hari)
  const eventDurationDays = differenceInDays(eventEnd, eventStart) + 1;

  // Konversi menjadi persentase
  const left = (daysFromStart / totalDays) * 100;
  const width = (eventDurationDays / totalDays) * 100;

  return { 
    left: Math.max(0, left), 
    width: Math.max(0, width),
  };
};

const goToDetail = (id) => {
  router.push(`/aktivitas/detail/${id}`);
};
</script>