<script setup lang="ts">
import TaskCard from "@/components/TaskCard.vue";
</script>

<template>
  <div class="px-5">
    <div class="mt-4 text-center">
      <p class="text-7xl">🐽</p>
      <p class="text-4xl">Earn more coins</p>
    </div>
    <div class="mt-5">
      <TaskCard v-for="i in 6" :key="i" />
    </div>
  </div>
</template>

<style scoped></style>
