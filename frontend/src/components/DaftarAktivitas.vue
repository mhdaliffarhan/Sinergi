<template>
  <div>
    <KartuAktivitas
      v-for="item in aktivitas"
      :key="item.id"
      v-bind="item"
    />
  </div>
</template>

<script setup>
import KartuAktivitas from '@/components/KartuAktivitas.vue';

// Bagian script ini sudah benar dan tidak perlu diubah.
defineProps({
  aktivitas: {
    type: Array, 
    required: true, 
  },
});
</script>