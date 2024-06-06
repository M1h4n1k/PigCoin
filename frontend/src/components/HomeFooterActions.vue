<script setup lang="ts"></script>

<template>
  <div class="flex items-center justify-between">
    <div class="flex items-center">
      <img
        alt="⚡️"
        class="h-10 w-10"
        src="https://freepngimg.com/save/141596-energy-symbol-free-download-png-hd/512x512"
      />
      <div class="flex flex-col">
        <span class="text-lg font-bold">1000</span>
        <span class="-mt-2 text-base font-semibold text-gray-500">/1000</span>
      </div>
    </div>
    <div
      class="flex h-14 w-fit items-center justify-center rounded-xl bg-gray-300"
    >
      <RouterLink to="/frens" class="flex w-20 flex-col items-center">
        <span>🐷</span>
        <span class="font-semibold">Frens</span>
      </RouterLink>
      <div class="h-[70%] border border-gray-400"></div>
      <RouterLink to="/tasks" class="flex w-20 flex-col items-center">
        <span>📋</span>
        <span class="font-semibold">Tasks</span>
      </RouterLink>
      <div class="h-[70%] border border-gray-400"></div>
      <RouterLink to="/boosts" class="flex w-20 flex-col items-center">
        <span>🚀</span>
        <span class="font-semibold">Boosts</span>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped></style>
