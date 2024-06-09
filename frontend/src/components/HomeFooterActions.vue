<script setup lang="ts">
import { useUserStore } from "@/store";
import { storeToRefs } from "pinia";

const userStore = useUserStore();
const { user } = storeToRefs(userStore);
</script>

<template>
  <div class="flex items-center justify-between">
    <div class="flex items-center">
      <img alt="🧼" class="h-10 w-10" src="/bathroom.svg" />
      <div class="flex flex-col">
        <span
          class="my-2 block h-6 w-14 animate-pulse rounded-lg bg-gray-200 p-2"
          v-if="user === null"
        ></span>
        <span v-else class="text-lg font-bold">{{ user.current_energy }}</span>
        <span class="-mt-2 flex text-base font-semibold text-gray-500"
          >/
          <span
            class="ml-0.5 mt-0.5 block h-5 w-12 animate-pulse rounded-lg bg-gray-200"
            v-if="user === null"
          ></span>
          <span v-else>{{ user.max_energy }}</span>
        </span>
      </div>
    </div>
    <div
      class="flex h-16 w-fit items-center justify-center rounded-xl bg-gray-200"
    >
      <RouterLink to="/frens" class="flex w-20 flex-col items-center">
        <img src="/pigsHead.png" alt="🐷" class="h-7 w-7" />
        <span class="font-semibold">Frens</span>
      </RouterLink>
      <div class="h-[70%] border border-gray-400"></div>
      <RouterLink to="/tasks" class="flex w-20 flex-col items-center">
        <img src="/clipboard.png" alt="📋" class="h-7 w-7" />
        <span class="font-semibold">Tasks</span>
      </RouterLink>
      <div class="h-[70%] border border-gray-400"></div>
      <RouterLink to="/boosts" class="flex w-20 flex-col items-center">
        <img src="/rocket.webp" alt="🚀" class="h-7 w-7" />
        <span class="font-semibold">Boosts</span>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped></style>
