<script setup lang="ts">
import { useUserStore } from "@/store.ts";
const userStore = useUserStore();

import BarnIcon from "@/components/BarnIcon.vue";
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
        <span
          >{{ userStore.user!.club!.members_count }}
          {{ $t("common.members", userStore.user!.club!.members_count) }}</span
        >
      </div>
    </div>
    <div class="flex flex-col items-center">
      <BarnIcon :league="userStore.user!.club?.league" class="h-12 w-12" />
    </div>
  </RouterLink>
</template>

<style scoped></style>
