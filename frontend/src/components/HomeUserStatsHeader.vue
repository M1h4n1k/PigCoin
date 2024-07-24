<script setup lang="ts">
import { useUserStore } from "@/store";
import { storeToRefs } from "pinia";
import FarmerIcon from "@/components/FarmerIcon.vue";
import IconArrowRight from "@/components/IconArrowRight.vue";

const userStore = useUserStore();
const { user } = storeToRefs(userStore);
</script>

<template>
  <div class="flex flex-col items-center">
    <div class="flex items-center text-5xl font-semibold">
      <span
        class="block h-12 w-40 animate-pulse rounded-lg bg-slate-200 p-2"
        v-if="user === null"
      ></span>
      <span v-else class="flex items-center">
        {{ user.current_coins.toLocaleString() }}
        <img src="/pigNoseCoin.svg" alt="🐽" class="ml-1 h-9 w-9"
      /></span>
    </div>
    <RouterLink to="/rating" class="relative flex items-center justify-center">
      <span class="text-lg font-semibold">#{{ userStore.user?.position }}</span>
      <span class="mx-5 text-3xl font-semibold">·</span>
      <div class="flex items-center">
        <FarmerIcon
          v-if="userStore?.user?.league"
          class="h-8 w-8"
          :league="userStore.user.league"
        />
      </div>
      <IconArrowRight
        height="20px"
        width="20px"
        class="absolute -right-[24px]"
      />
    </RouterLink>
  </div>
</template>

<style scoped></style>
