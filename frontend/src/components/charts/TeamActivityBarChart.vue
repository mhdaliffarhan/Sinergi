<template>
  <div>
    <VueApexCharts 
      type="bar" 
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
      type: 'bar',
      height: 350,
      stacked: true,
      toolbar: { show: false },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '55%',
      },
    },
    dataLabels: {
      enabled: false
    },
    stroke: {
      show: true,
      width: 2,
      colors: ['transparent']
    },
    xaxis: {
      categories: props.categories,
      labels: {
        style: {
          colors: labelColor,
        },
      },
    },
    yaxis: {
      title: {
        text: 'Jumlah Aktivitas',
        style: {
          color: labelColor,
        }
      },
      labels: {
        style: {
          colors: labelColor,
        },
      },
    },
    grid: {
      borderColor: gridColor,
    },
    fill: {
      opacity: 1
    },
    legend: {
      position: 'top',
      horizontalAlign: 'left',
      labels: {
        colors: labelColor,
      }
    },
    colors: ['#22c55e', '#f97316'], // Hijau & Oranye
  };
});
</script>