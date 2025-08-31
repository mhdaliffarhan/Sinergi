<template>
  <div>
    <KartuProject
      v-for="item in projects"
      :key="item.id"
      v-bind="item"
    />
  </div>
</template>

<script setup>
import KartuProject from '@/components/project/KartuProject.vue';

defineProps({
  projects: {
    type: Array, 
    required: true, 
  },
});
</script>