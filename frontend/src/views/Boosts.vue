<script setup lang="ts">
import Booster from "@/components/Booster.vue";
</script>

<template>
  <div class="px-5 py-2">
    <div class="text-center">
      <p class="text-lg">Balance</p>
      <p class="text-4xl font-medium">🐽132 456</p>
    </div>
    <div class="mt-5">
      <h3 class="text-xl">Free daily boosters</h3>
      <div class="mt-2 flex justify-around gap-4">
        <div
          class="flex w-1/2 items-center justify-between rounded-2xl border py-2 pl-4 pr-2"
        >
          <div>
            <p class="text-xl">Pig</p>
            <p class="text-gray-600">2/3 available</p>
          </div>
          <img height="50" width="50" src="/pig.png" alt="refill" />
        </div>

        <div
          class="flex w-1/2 items-center justify-between rounded-2xl border py-2 pl-4 pr-2"
        >
          <div>
            <p class="text-xl">Refill</p>
            <p class="text-gray-600">2/3 available</p>
          </div>
          <img height="60" width="60" src="/soapRefill.jpg" alt="refill" />
        </div>
      </div>
    </div>

    <div class="mt-5">
      <h3 class="text-xl">Boosters</h3>
      <div
        class="mt-2 flex flex-col justify-around gap-4 rounded-xl border p-5"
      >
        <Booster v-for="i in 5" :key="i" />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
