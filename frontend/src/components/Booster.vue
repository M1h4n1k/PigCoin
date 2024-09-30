<script setup lang="ts">
import { ref } from "vue";
import IconArrowRight from "@/components/IconArrowRight.vue";
import PopupWindow from "@/components/PopupWindow.vue";
import { useAlertStore, useBoostsStore, useUserStore } from "@/store.ts";
import { useI18n } from "vue-i18n";

const userStore = useUserStore();
const alertStore = useAlertStore();
const boostsStore = useBoostsStore();
const { t } = useI18n();

const props = defineProps({
  id: Number,
  title: String,
  description: String,
  picture: String,
  price: Number,
  count: Number,
});

const buyBoost = () => {
  if (
    userStore.user!.current_coins <
    boostsStore.boosts.find((b) => b.id === props.id)!.price
  ) {
    Telegram.WebApp.HapticFeedback.notificationOccurred("error");
    alertStore.displayAlert(t("error.no_coins"), "error");
    return;
  }

  boostsStore.boosts = boostsStore.boosts.map((b) => {
    if (b.id === props.id) {
      userStore.user!.current_coins -= b.price;
      b.count++;
      b.price += 100;
    }
    return b;
  });

  fetch(import.meta.env.VITE_API_URL + `/boosts/buy/${props.id}`, {
    method: "POST",
    credentials: "include",
  })
    .then((res) => {
      if (res.status === 402) {
        throw new Error("Not enough coins");
      }
      return res.json();
    })
    .catch((err) => {
      boostsStore.boosts = boostsStore.boosts.map((b) => {
        if (b.id === props.id) {
          b.count--;
          b.price -= 100;
          userStore.user!.current_coins += b.price;
        }
        return b;
      });
      console.log(err);
    });
};

const selected = ref(false);
</script>

<template>
  <div
    @click="() => (selected = true)"
    class="flex w-full items-center justify-between rounded-2xl"
  >
    <div class="flex items-center justify-center">
      <div
        class="toned-image-bg flex h-[70px] w-[70px] items-center justify-center rounded-xl p-2"
      >
        <img
          class="h-[50px] w-[50px]"
          height="50"
          width="50"
          :src="picture"
          alt="refill"
        />
      </div>
      <div class="ml-2">
        <p class="text-xl">{{ title }}</p>
        <p class="text-gray-600">
          {{ price }}
          <img class="mb-0.5 inline h-3 w-3" src="/pigNoseCoin.svg" alt="🐽" />
        </p>
      </div>
    </div>

    <IconArrowRight height="25px" width="25px" />

    <PopupWindow
      :style="{
        transform: selected ? 'translateY(0)' : 'translateY(100%)',
      }"
      class="fixed left-0"
      :header="title ?? ''"
      @close="() => (selected = false)"
    >
      <div class="flex">
        <img
          class="h-[60px] w-[60px]"
          height="60"
          width="60"
          :src="picture"
          alt="refill"
        />
        <div class="ml-5">
          <p>{{ description }}</p>
          <p class="font-bold">{{ $t("boosts.count") }}: {{ count }}</p>
        </div>
      </div>
      <button
        @click="buyBoost"
        class="mt-2 w-full rounded-xl border px-4 py-2 font-semibold"
      >
        {{ $t("boosts.buy") }}
      </button>
    </PopupWindow>
  </div>
</template>

<style scoped></style>
