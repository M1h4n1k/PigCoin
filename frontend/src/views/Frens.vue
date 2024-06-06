<script setup lang="ts">
import RatingUserCard from "@/components/RatingUserCard.vue";
</script>

<template>
  <div class="px-5 py-2">
    <h3 class="mt-10 text-center text-2xl font-medium">
      Invite Frens, get coins
    </h3>
    <div class="mt-3 space-y-4 rounded-xl border p-5">
      <div class="flex items-center">
        <img height="50" width="50" src="/pigNose.webp" alt="" />
        <div class="ml-4">
          <p class="text-lg font-medium">Invite fren</p>
          <p class="text-gray-600">2500 for you and your fren</p>
        </div>
      </div>

      <div class="flex items-center">
        <img height="50" width="50" src="/Telegram_Premium.png" alt="" />
        <div class="ml-4">
          <p class="text-lg font-medium">Invite fren with Premium</p>
          <p class="text-gray-600">25000 for you and your fren</p>
        </div>
      </div>
    </div>

    <h3 class="mt-10 text-center text-2xl font-medium">Frens</h3>
    <div class="mt-3 w-full space-y-3 rounded-xl border py-3">
      <RatingUserCard
        v-for="i in 4"
        :key="i"
        :rating="i"
        :coins="100000 * (10 - i)"
        :name="'user' + i"
      />
    </div>
  </div>
</template>

<style scoped></style>
