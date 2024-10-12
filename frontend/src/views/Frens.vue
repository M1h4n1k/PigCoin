<script setup lang="ts">
import { ref } from "vue";
import RatingUserCard from "@/components/RatingUserCard.vue";
import { useUserStore } from "@/store";
import LoadingIcon from "@/components/LoadingIcon.vue";
import { shareInviteLink } from "@/utils.ts";
import { vInfiniteScroll } from "@/directives.ts";

const userStore = useUserStore();
const loading = ref(false);
const isFullyLoaded = ref(false);

const loadReferrals = (offset = 0, limit = 20) => {
  if (loading.value || isFullyLoaded.value) return;
  loading.value = true;

  fetch(
    import.meta.env.VITE_API_URL +
      `/user/referrals?offset=${offset}&limit=${limit}`,
    {
      credentials: "include",
    },
  )
    .then((res) => res.json())
    .then((data) => {
      if (data.length === 0 || data.length < limit) isFullyLoaded.value = true;
      userStore.referrals.push(...data);
      loading.value = false;
    })
    .catch((err) => {
      console.log(err);
    });
};

if (userStore.referrals.length === 0) {
  loadReferrals();
}
</script>

<template>
  <div class="px-3 py-2 pb-4">
    <div class="toned-bg mt-2 space-y-4 rounded-xl p-3">
      <h3 class="text-center text-2xl font-medium">{{ $t("frens.earn") }}</h3>
      <div class="flex items-center">
        <img height="50" width="50" src="/pigNose.webp" alt="" />
        <div class="ml-4">
          <p class="text-lg font-medium">{{ $t("frens.invite") }}</p>
          <p class="text-gray-600">
            {{ (2500).toLocaleString() }} {{ $t("frens.invite.desc") }}
          </p>
        </div>
      </div>

      <div class="flex items-center">
        <img height="50" width="50" src="/Telegram_Premium.png" alt="" />
        <div class="ml-4">
          <p class="text-lg font-medium leading-5">
            {{ $t("frens.premium") }}
          </p>
          <p class="text-gray-600">
            {{ (25000).toLocaleString() }} {{ $t("frens.invite.desc") }}
          </p>
        </div>
      </div>
    </div>

    <button
      @click="shareInviteLink('user')"
      class="mt-4 w-full rounded-full bg-[#2481cc] px-5 py-2 font-semibold text-white hover:!bg-[#1a8ad5]"
    >
      {{ $t("frens.invite.cta") }}
    </button>

    <div
      v-infinite-scroll="() => loadReferrals(userStore.referrals.length)"
      class="toned-bg mt-10 w-full rounded-xl py-3"
    >
      <h3 class="px-5 text-start text-2xl font-medium">
        {{ $t("common.frens") }}
      </h3>
      <RatingUserCard
        v-for="(referral, ix) in userStore.referrals"
        :key="ix"
        :picture="referral.picture"
        :rating="ix + 1"
        :coins="referral.total_coins"
        :name="referral.username"
      />
      <div v-if="loading" class="flex w-full items-center justify-center p-2">
        <LoadingIcon />
      </div>
      <div
        v-if="userStore.referrals.length === 0 && !loading"
        class="block w-full text-center text-lg"
      >
        {{ $t("common.no_data") }}
      </div>
    </div>
  </div>
</template>

<style scoped></style>
