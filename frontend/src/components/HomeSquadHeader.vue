<script setup lang="ts">
import { useUserStore } from "@/store.ts";
const userStore = useUserStore();

import BarnIcon from "@/components/BarnIcon.vue";
</script>

<template>
  <div
    v-if="!userStore.user"
    class="toned-bg h-12 w-full animate-pulse rounded-xl px-5 py-2"
  />
  <RouterLink
    v-else-if="userStore.user?.club"
    to="/club"
    class="toned-bg flex w-full cursor-pointer items-center justify-between rounded-xl px-5 py-2"
  >
    <div class="flex items-center">
      <img
        class="h-12 w-12 rounded-lg"
        :src="userStore.user.club.picture"
        alt=""
      />
      <div class="ml-2 flex flex-col items-start justify-center">
        <span class="text-lg font-bold">{{ userStore.user!.club!.name }}</span>
        <span
          >{{ userStore.user!.club!.members_count }}
          {{ $t("common.members", userStore.user!.club!.members_count) }}</span
        >
      </div>
    </div>
    <div class="flex flex-col items-center">
      <BarnIcon :league="userStore.user.club.league" class="h-12 w-12" />
    </div>
  </RouterLink>

  <RouterLink
    v-else
    to="/createClub"
    class="toned-bg flex h-14 w-full cursor-pointer items-center justify-start rounded-xl px-5 py-2"
  >
    <svg class="mr-2" height="30px" width="30px" viewBox="0 0 100 100">
      <path
        d="M25.0 29.0L25.0 29.0Q25.0 27.0 26.2 25.0Q27.3 23.0 29.2 21.8Q31.0 20.7 33.3 20.7Q35.7 20.7 37.5 21.8Q39.3 23.0 40.5 25.0Q41.7 27.0 41.7 29.0L41.7 29.0Q41.7 32.7 39.2 35.0Q36.7 37.3 33.3 37.3Q30.0 37.3 27.5 35.0Q25.0 32.7 25.0 29.0ZM33.3 12.3L33.3 12.3Q26.3 12.3 21.5 17.3Q16.7 22.3 16.7 29.2Q16.7 36 21.5 40.8Q26.3 45.7 33.3 45.7Q40.3 45.7 45.2 40.8Q50.0 36 50.0 29.2Q50.0 22.3 45.2 17.3Q40.3 12.3 33.3 12.3ZM9.7 66.3L9.7 66.3Q13.0 63.3 17.7 61.3L17.7 61.3Q24.3 58.3 33.3 58.3Q42.3 58.3 49.0 61.3L49.0 61.3Q53.7 63.3 57.0 66.3L57.0 66.3Q58.3 67.7 58.3 71L58.3 71Q58.3 72.7 57.2 73.8Q56.0 75 54.3 75L54.3 75L12.3 75Q10.7 75 9.5 73.8Q8.3 72.7 8.3 71L8.3 71Q8.3 67.7 9.7 66.3ZM33.3 50.0L33.3 50.0Q22.7 50.0 14.3 53.7L14.3 53.7Q8.3 56.0 4.2 60.2Q0 64.3 0 71L0 71Q0 76 3.7 79.7Q7.3 83.3 12.3 83.3L12.3 83.3L54.3 83.3Q59.3 83.3 63.0 79.7Q66.7 76 66.7 71L66.7 71Q66.7 64.3 62.5 60.2Q58.3 56.0 52.3 53.7L52.3 53.7Q44.0 50.0 33.3 50.0ZM68.7 57.7L68.7 57.7Q68.7 56.0 70.0 54.8Q71.3 53.7 73.0 53.7L73.0 53.7Q81.3 54.0 88.0 57.0L88.0 57.0Q93.0 59.3 96.5 62.8Q100.0 66.3 100.0 72L100.0 72Q100.0 76.7 96.7 80Q93.3 83.3 88.7 83.3L88.7 83.3L75.0 83.3Q73.3 83.3 72.2 82.2Q71.0 81 71.0 79.2Q71.0 77.3 72.2 76.2Q73.3 75 75.0 75L75.0 75L88.7 75Q90.0 75 90.8 74.2Q91.7 73.3 91.7 72L91.7 72Q91.7 69.7 90.7 68.7L90.7 68.7Q84.3 62.3 72.7 62.0L72.7 62.0Q71.0 62.0 69.8 60.7Q68.7 59.3 68.7 57.7ZM64.7 35.3L64.7 35.3Q64.7 33.7 65.5 32.2Q66.3 30.7 67.7 29.8Q69.0 29.0 70.8 29.0Q72.7 29.0 74.0 29.8Q75.3 30.7 76.2 32.2Q77.0 33.7 77.0 35.3L77.0 35.3Q77.0 38.0 75.2 39.8Q73.3 41.7 70.8 41.7Q68.3 41.7 66.5 39.8Q64.7 38.0 64.7 35.3ZM71.0 21.0L71.0 21.0Q64.7 21.0 60.5 25.2Q56.3 29.3 56.3 35.3Q56.3 41.3 60.5 45.7Q64.7 50.0 70.8 50.0Q77.0 50.0 81.2 45.7Q85.3 41.3 85.3 35.3Q85.3 29.3 81.2 25.2Q77.0 21.0 71.0 21.0Z"
      ></path>
    </svg>
    <span class="text-lg">{{ $t("club.create") }}</span>
  </RouterLink>
</template>

<style scoped></style>
