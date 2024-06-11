<script setup lang="ts">
import { useUserStore } from "@/store.ts";
const userStore = useUserStore();
</script>

<template>
  <RouterLink
    to="/club"
    class="toned-bg flex w-full cursor-pointer items-center justify-between rounded-xl px-5 py-2"
  >
    <div class="flex items-center">
      <img class="h-10 w-10" :src="userStore.user!.club!.picture" alt="" />
      <div class="ml-2 flex flex-col items-start justify-center">
        <span class="text-lg font-bold">{{ userStore.user!.club?.name }}</span>
        <span>{{ userStore.user!.club!.total_coins }} coins</span>
      </div>
    </div>
    <div class="flex flex-col items-center">
      <div class="h-8 w-8 bg-emerald-500"></div>
      <span class="">Emerald</span>
    </div>
  </RouterLink>
</template>

<style scoped></style>
