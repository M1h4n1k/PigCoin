<script setup lang="ts">
import RatingUserCard from "@/components/RatingUserCard.vue";
import { useUserStore } from "@/store";

const userStore = useUserStore();
if (userStore.referrals.length === 0) {
  fetch(import.meta.env.VITE_API_URL + "/user/referrals", {
    credentials: "include",
  })
    .then((res) => res.json())
    .then((data) => {
      userStore.referrals = data;
    })
    .catch((err) => {
      console.log(err);
    });
}
</script>

<template>
  <div class="px-5 py-2">
    <div class="toned-bg mt-10 space-y-4 rounded-xl p-5">
      <h3 class="text-center text-2xl font-medium">Invite Frens, get coins</h3>
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

    <button class="mt-5 w-full rounded-xl border p-2">Invite frens</button>

    <h3 class="mt-10 text-center text-2xl font-medium">Frens</h3>
    <div class="toned-bg mt-3 w-full space-y-3 rounded-xl py-3">
      <RatingUserCard
        v-for="(referral, ix) in userStore.referrals"
        :key="ix"
        :picture="referral.picture"
        :rating="ix + 1"
        :coins="referral.total_coins"
        :name="referral.username"
      />
      <span
        v-if="userStore.referrals.length === 0"
        class="block w-full text-center text-lg"
      >
        No frens yet
      </span>
    </div>
  </div>
</template>

<style scoped></style>
