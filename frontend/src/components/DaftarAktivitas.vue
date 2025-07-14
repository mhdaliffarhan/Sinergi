<template>
  <div>
    <KartuAktivitas
      v-for="item in aktivitas"
      :key="item.id"
      :nama_aktivitas="item.nama"
      :tanggal="item.tanggal"
      :nama_tim="item.tim"
      :jumlah_dokumen="item.dokumen"
    />
  </div>
</template>

<script setup>
import KartuAktivitas from '@/components/KartuAktivitas.vue';
defineProps({
  aktivitas: {
    type: Array, 
    required: true, 
  },
});
</script>