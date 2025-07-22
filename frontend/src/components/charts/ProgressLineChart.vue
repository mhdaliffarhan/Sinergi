<template>
  <div>
    <VueApexCharts 
      type="area" 
      height="350"
      :options="chartOptions" 
      :series="series"
    ></VueApexCharts>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import VueApexCharts from 'vue3-apexcharts';

const props = defineProps({
  series: {
    type: Array,
    required: true
  },
  categories: {
    type: Array,
    required: true
  }
});

const chartOptions = computed(() => {
  const isDarkMode = document.documentElement.classList.contains('dark');
  const gridColor = isDarkMode ? '#4a5568' : '#e5e7eb';
  const labelColor = isDarkMode ? '#cbd5e1' : '#6b7280';

  return {
    chart: {
      height: 350,
      type: 'area',
      toolbar: { show: false },
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'smooth'
    },
    xaxis: {
      type: 'category',
      categories: props.categories,
      labels: {
        style: {
          colors: labelColor,
        },
      },
    },
    yaxis: {
      labels: {
        style: {
          colors: labelColor,
        },
      },
    },
    grid: {
      borderColor: gridColor,
    },
    legend: {
      labels: {
        colors: labelColor,
      },
    },
    colors: ['#3b82f6', '#16a34a'], // Biru untuk Aktivitas, Hijau untuk Dokumen
  };
});
</script>