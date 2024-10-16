<script setup lang="ts">
import { ref, computed } from "vue";
import { Decoration } from "@/types.ts";
import { useUserStore, useAlertStore } from "@/store.ts";
import IconAlertInfo from "@/components/IconAlertInfo.vue";

const userStore = useUserStore();
const alertStore = useAlertStore();

const decoration = ref<Decoration | undefined | null>(undefined);

const amount = ref<string | undefined>(undefined);

const validateAmount = computed(() => {
  if (amount.value === undefined) return 1;
  if (
    amount.value === "" ||
    parseInt(amount.value) <= decoration.value!.last_bet
  )
    return -1;
  return 0;
});

fetch(import.meta.env.VITE_API_URL + "/decorations", {
  credentials: "include",
})
  .then((res) => {
    if (!res.ok) {
      throw new Error(res.statusText);
    }
    return res.json();
  })
  .then((data: Decoration | null) => {
    decoration.value = data;
  })
  .catch((err) => {
    console.log(err);
  });

const makeBet = () => {
  if (amount.value === undefined) amount.value = "";
  if (validateAmount.value !== 0) return;
  fetch(import.meta.env.VITE_API_URL + "/decorations/bet", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      amount: parseInt(amount.value!),
      decoration_id: decoration.value!.id,
    }),
  })
    .then((res) => {
      if (!res.ok) {
        console.log(res.statusText);
      }
      return res.json();
    })
    .then((data: Decoration) => {
      userStore.user!.current_coins -= parseInt(amount.value!);
      if (decoration.value!.last_bet_user.uid === userStore.user!.uid) {
        userStore.user!.current_coins += decoration.value!.last_bet;
      }
      decoration.value = data;
      amount.value = undefined;
    })
    .catch((err) => {
      console.log(err);
      alertStore.displayAlert(err, "error");
    });
};
</script>

<template>
  <div class="px-2 pt-10">
    <p v-if="decoration === null">No decoration</p>
    <p v-else-if="decoration === undefined">Loading...</p>
    <div v-else class="flex flex-col items-center">
      <div class="toned-bg flex w-full flex-col items-center px-3 pb-3 pt-7">
        <div class="relative h-20 w-20 rounded-full bg-gray-200">
          <img
            :src="userStore.user!.picture"
            alt=""
            class="h-20 w-20 rounded-full"
          />
          <img class="absolute -top-12" :src="decoration.picture" alt="" />
        </div>
        <p class="text-3xl">{{ decoration.title }}</p>
        <!--        <p class="mt-2 text-lg">Decoration for user picture</p>-->
        <p class="mt-2 text-lg">
          {{ $t("auction.ends_at") }}
          {{ new Date(decoration.betting_ends_at * 1000).toLocaleString() }}
        </p>
      </div>

      <div class="toned-bg mt-3 w-full px-3 py-3">
        <p class="flex items-center text-lg">
          {{ $t("auction.last_bet") }}: {{ decoration.last_bet
          }}<img
            class="ml-1 h-3 w-3"
            src="/pigNoseCoin.svg"
            alt="🐽"
            loading="lazy"
          />
        </p>

        <div class="mt-1 flex w-full" v-if="decoration.last_bet_user">
          <span class="">{{ $t("auction.last_user") }}:</span>
          <div class="ml-3 flex items-center">
            <img
              :src="decoration.last_bet_user.picture"
              alt=""
              class="aspect-square h-5 w-5 rounded-full"
            />
            <p class="ml-1 w-36 truncate">
              {{ decoration.last_bet_user.username }}
            </p>
          </div>
        </div>

        <input
          class="mt-2 w-full rounded-lg border-2 px-3 py-2 outline-none"
          :style="{
            borderColor: validateAmount === -1 ? '#ff4141' : '',
          }"
          type="number"
          :placeholder="$t('frens.transactions.input_amount')"
          v-model="amount"
        />

        <button
          @click="makeBet"
          class="mt-3 w-full rounded-full bg-[#2481cc] px-5 py-2 font-semibold text-white hover:!bg-[#1a8ad5]"
        >
          {{ $t("auction.bet") }}
        </button>
      </div>

      <div class="toned-bg mt-3 px-3 py-3">
        <IconAlertInfo class="mr-1 inline text-gray-400" />
        {{ $t("auction.explain") }}
      </div>
    </div>
  </div>
</template>

<style scoped></style>
