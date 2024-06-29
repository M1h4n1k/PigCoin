<script setup lang="ts">
import { useUserStore } from "@/store";

const userStore = useUserStore();
</script>

<template>
  <div class="flex items-center justify-between">
    <div class="toned-bg flex h-full items-center rounded-xl px-2 pl-3">
      <img alt="🧼" class="-ml-3 h-11 w-11" src="/bottle.png" />
      <div class="flex flex-col">
        <span
          class="mb-2 block h-5 w-14 animate-pulse rounded-lg bg-gray-200 p-2"
          v-if="userStore.user === null"
        ></span>
        <span v-else class="text-lg font-bold">{{
          userStore.user.current_energy
        }}</span>
        <span
          class="-mt-2 flex items-center text-base font-semibold text-gray-500"
          >/
          <span
            class="ml-1 mt-0.5 h-[15px] w-12 animate-pulse rounded-md bg-gray-200"
            v-if="userStore.user === null"
          ></span>
          <span v-else>{{ userStore.user.max_energy }}</span>
        </span>
      </div>
    </div>
    <div
      class="toned-bg flex h-16 w-fit items-center justify-center rounded-xl"
    >
      <RouterLink to="/frens" class="flex w-20 flex-col items-center">
        <img src="/pigsHead.png" alt="🐷" class="h-7 w-7" />
        <span class="font-semibold">{{ $t("common.frens") }}</span>
      </RouterLink>
      <div class="h-[70%] border border-gray-400/40"></div>
      <RouterLink to="/tasks" class="flex w-20 flex-col items-center">
        <img src="/clipboard.png" alt="📋" class="h-7 w-7" />
        <span class="font-semibold">{{ $t("common.tasks") }}</span>
      </RouterLink>
      <div class="h-[70%] border border-gray-400/40"></div>
      <RouterLink to="/boosts" class="flex w-20 flex-col items-center">
        <img src="/rocket.webp" alt="🚀" class="h-7 w-7" />
        <span class="font-semibold">{{ $t("common.boosts") }}</span>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped></style>
