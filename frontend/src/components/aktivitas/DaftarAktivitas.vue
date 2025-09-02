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
import KartuAktivitas from '@/components/aktivitas/KartuAktivitas.vue';

defineProps({
  aktivitas: {
    type: Array, 
    required: true, 
  },
});
</script>