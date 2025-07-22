<template>
  <div>
    <VueApexCharts 
      type="donut" 
      height="350"
      :options="chartOptions" 
      :series="series"
    ></VueApexCharts>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

// Komponen ini menerima data 'series' dan 'labels' dari parent
const props = defineProps({
  series: {
    type: Array,
    required: true
  },
  labels: {
    type: Array,
    required: true
  }
});

// Opsi untuk mengatur tampilan chart
const chartOptions = computed(() => {
  // Cek tema dark mode saat ini
  const isDarkMode = document.documentElement.classList.contains('dark');

  return {
    chart: {
      type: 'donut',
    },
    labels: props.labels,
    colors: ['#22c55e', '#f97316'], // Hijau untuk Selesai, Oranye untuk Belum Lengkap
    legend: {
      position: 'bottom',
      labels: {
        // Sesuaikan warna teks legenda untuk dark mode
        colors: isDarkMode ? '#cbd5e1' : '#4b5563'
      }
    },
    responsive: [{
      breakpoint: 480,
      options: {
        chart: {
          width: 200
        },
        legend: {
          position: 'bottom'
        }
      }
    }],
    // Menampilkan persentase di dalam chart
    dataLabels: {
      enabled: true,
      formatter: function (val, opts) {
        return `${opts.w.globals.seriesNames[opts.seriesIndex]}: ${Math.round(val)}%`
      },
    },
  };
});
</script>