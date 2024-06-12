<script setup lang="ts">
import { useUserStore } from "@/store";
import { storeToRefs } from "pinia";
import FarmerIcon from "@/components/FarmerIcon.vue";

const userStore = useUserStore();
const { user } = storeToRefs(userStore);
</script>

<template>
  <div class="flex flex-col items-center">
    <div class="flex items-center text-5xl font-semibold">
      <span
        class="block h-12 w-40 animate-pulse rounded-lg bg-gray-200 p-2"
        v-if="user === null"
      ></span>
      <span v-else class="flex items-center">
        {{ user.current_coins }}
        <img src="/pigNoseCoin.svg" alt="🐽" class="h-9 w-9"
      /></span>
    </div>
    <RouterLink to="/rating" class="relative flex items-center justify-center">
      <span class="text-lg font-semibold">#{{ userStore.user?.position }}</span>
      <span class="mx-5 text-3xl font-semibold">·</span>
      <div class="flex items-center">
        <FarmerIcon class="h-8 w-8" :league="userStore.user?.league" />
      </div>
      <svg
        class="absolute -right-[24px]"
        height="20px"
        width="20px"
        viewBox="0 0 100 100"
      >
        <path
          d="M40.0 21.7L65.3 47.0Q66.7 48.3 66.7 49.8Q66.7 51.3 65.7 52.7L65.7 52.7L40.3 78Q39.3 79 37.7 79.2Q36.0 79.3 34.7 78.2Q33.3 77 33.3 75.3Q33.3 73.7 34.3 72.3L34.3 72.3L56.7 50.0L34.7 28.0Q33.3 27.0 33.3 25.3Q33.3 23.7 34.3 22.3L34.3 22.3L34.7 22.0Q35.7 21.0 37.2 20.8Q38.7 20.7 40.0 21.7L40.0 21.7Z"
        ></path>
      </svg>
    </RouterLink>
  </div>
</template>

<style scoped></style>
