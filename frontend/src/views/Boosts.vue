<script setup lang="ts">
import { ref } from "vue";
import Booster from "@/components/Booster.vue";
import { useUserStore, useBoostsStore, useAlertStore } from "@/store";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import LoadingIcon from "@/components/LoadingIcon.vue";

const router = useRouter();
const { t } = useI18n();

const userStore = useUserStore();
const alertStore = useAlertStore();
const boostsStore = useBoostsStore();
const loading = ref(boostsStore.boosts.length === 0);

if (boostsStore.boosts.length === 0) {
  fetch(import.meta.env.VITE_API_URL + "/boosts/", {
    credentials: "include",
  })
    .then((res) => res.json())
    .then((data) => {
      boostsStore.boosts = data;
      loading.value = false;
    });
}

const buyBoost = (boostId: number) => {
  if (
    userStore.user!.current_coins <
    boostsStore.boosts.find((b) => b.id === boostId)!.price
  ) {
    Telegram.WebApp.HapticFeedback.notificationOccurred("error");
    alertStore.displayAlert(t("error.no_coins"), "error");
    return;
  }

  fetch(import.meta.env.VITE_API_URL + `/boosts/buy/${boostId}`, {
    method: "POST",
    credentials: "include",
  })
    .then((res) => {
      if (res.status === 402) {
        throw new Error("Not enough coins");
      }
      return res.json();
    })
    .then((data) => {
      userStore.user = data;
      boostsStore.boosts = boostsStore.boosts.map((b) => {
        if (b.id === boostId) {
          b.count++;
          b.price += 100;
        }
        return b;
      });
    })
    .catch((err) => {
      console.log(err);
    });
};

const useFreeBooster = (type: number) => {
  if (type === 0 && userStore.user!.free_turbo === 0) {
    Telegram.WebApp.HapticFeedback.notificationOccurred("error");
    alertStore.displayAlert(t("error.no_boost"), "error");
    return;
  }
  if (type === 1 && userStore.user!.free_refills === 0) {
    Telegram.WebApp.HapticFeedback.notificationOccurred("error");
    alertStore.displayAlert(t("error.no_boost"), "error");
    return;
  }
  fetch(import.meta.env.VITE_API_URL + `/boosts/use/${type}`, {
    method: "POST",
    credentials: "include",
  }).then(() => {
    if (type === 0) {
      userStore.user!.free_turbo--;
      router.push("/minigame");
    } else {
      userStore.user!.free_refills--;
      userStore.user!.current_energy = userStore.user!.max_energy;
      router.push("/");
    }
  });
};
</script>

<template>
  <div class="px-3 py-2 pb-4">
    <div class="p-3 text-center">
      <p class="text-3xl">{{ $t("boosts.balance") }}</p>
      <p class="flex items-center justify-center text-4xl font-medium">
        <span>{{ userStore.user?.current_coins.toLocaleString() }}</span>
        <img class="ml-1 inline h-6 w-6" src="/pigNoseCoin.svg" alt="🐽" />
      </p>
    </div>

    <div class="toned-bg px-3 py-3">
      <h3 class="text-2xl font-medium">{{ $t("boosts.free") }}</h3>
      <div class="mt-2 flex justify-around gap-2">
        <div
          class="toned-image-bg flex w-1/2 cursor-pointer items-center justify-between rounded-2xl px-2 py-2"
          @click="useFreeBooster(0)"
        >
          <div>
            <p class="text-xl">{{ $t("boosts.pigfall") }}</p>
            <p class="flex items-center text-gray-600">
              <span>{{ userStore.user?.free_turbo }}</span
              >/3 {{ $t("boosts.available") }}
            </p>
          </div>
          <img height="32" width="32" src="/pigFall.svg" alt="refill" />
        </div>

        <div
          class="toned-image-bg flex w-1/2 cursor-pointer items-center justify-between rounded-2xl px-2 py-2"
          @click="useFreeBooster(1)"
        >
          <div>
            <p class="text-xl">{{ $t("boosts.refill") }}</p>
            <p class="flex items-center text-gray-600">
              <span>{{ userStore.user?.free_refills }}</span
              >/3 {{ $t("boosts.available") }}
            </p>
          </div>
          <img height="40" width="40" src="/refill.png" alt="refill" />
        </div>
      </div>
    </div>

    <div class="mt-5">
      <div
        class="toned-bg mt-2 flex flex-col justify-around gap-4 rounded-xl p-3"
      >
        <h3 class="text-2xl font-medium">{{ $t("boosts") }}</h3>
        <Booster
          class="cursor-pointer"
          v-for="b in boostsStore.boosts"
          :key="b.id"
          :picture="b.picture"
          :title="$t('boosts.' + b.title.toLowerCase().replace(' ', '_'))"
          :price="b.price"
          @click="buyBoost(b.id)"
        />

        <div v-if="loading" class="flex w-full items-center justify-center p-2">
          <LoadingIcon />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped></style>
