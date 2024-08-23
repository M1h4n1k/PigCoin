<script setup lang="ts">
import IconAlertInfo from "@/components/IconAlertInfo.vue";
import IconAlertError from "@/components/IconAlertError.vue";
import { useAlertStore } from "@/store.ts";

const alertStore = useAlertStore();
</script>

<template>
  <div
    class="pointer-events-none fixed top-3 z-50 flex w-full items-center justify-center px-2 opacity-0 transition-opacity duration-300"
    :class="{
      '!opacity-100': alertStore.isDisplayed,
    }"
  >
    <div
      class="flex h-fit min-h-[45px] w-full select-none items-center rounded-xl bg-gray-800 py-2 pl-2"
    >
      <IconAlertError v-if="alertStore.type === 'error'" />
      <IconAlertInfo class="ml-[10px]" v-else-if="alertStore.type === 'info'" />
      <span class="ml-[5px] w-full text-white">{{ alertStore.message }}</span>
    </div>
  </div>
</template>

<style scoped></style>
