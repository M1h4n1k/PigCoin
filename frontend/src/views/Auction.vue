<script setup lang="ts">
import { ref, computed, onUnmounted } from "vue";
import { Decoration } from "@/types.ts";
import { useUserStore, useAlertStore, useAuctionStore } from "@/store.ts";
import IconAlertInfo from "@/components/IconAlertInfo.vue";
import LoadingIcon from "@/components/LoadingIcon.vue";

const userStore = useUserStore();
const alertStore = useAlertStore();
const auctionStore = useAuctionStore();

const decoration = computed(() => {
  if (auctionStore.decorations.length === 0) return null;
  return auctionStore.decorations[0];
});

const currentDate = ref(Date.now() / 1000);

const updaterInterval = setInterval(() => {
  fetch(import.meta.env.VITE_API_URL + "/decorations/", {
    credentials: "include",
  })
    .then((res) => res.json())
    .then((data: Decoration | null) => {
      if (!data) {
        clearInterval(updaterInterval);
        return;
      }
      auctionStore.decorations[0] = data;
    });
}, 5000);

const timerInterval = setInterval(() => {
  currentDate.value = Date.now() / 1000;
}, 1000);

onUnmounted(() => {
  clearInterval(timerInterval);
  if (updaterInterval) clearInterval(updaterInterval);
});

const timeLeft = computed(() => {
  return decoration.value!.betting_ends_at - currentDate.value;
});

const formattedTimeLeft = computed(() => {
  return (
    Math.floor(timeLeft.value / 60 / 60)
      .toString()
      .padStart(2, "0") +
    ":" +
    Math.floor((timeLeft.value % 3600) / 60)
      .toString()
      .padStart(2, "0") +
    ":" +
    Math.floor(timeLeft.value % 60)
      .toString()
      .padStart(2, "0")
  );
});

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
      auctionStore.decorations[0] = data;
      amount.value = undefined;
    })
    .catch((err) => {
      console.log(err);
      alertStore.displayAlert(err, "error");
    });
};
</script>

<template>
  <div class="px-2 pt-6">
    <p class="toned-bg p-3 text-center text-lg" v-if="decoration === null">
      {{ $t("auction.no") }}
    </p>
    <p class="flex w-full justify-center" v-else-if="decoration === undefined">
      <LoadingIcon />
    </p>
    <div v-else class="flex flex-col items-center">
      <div class="toned-bg flex w-full flex-col items-center px-3 pb-3 pt-9">
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
        <p v-if="timeLeft > 0" class="mt-2 text-lg">
          {{ $t("auction.ends_at") }}
          {{ formattedTimeLeft }}
        </p>

        <div v-else class="mt-2 flex text-lg">
          {{ $t("auction.winner") }}:
          <div class="ml-1 flex items-center">
            <img
              :src="decoration.last_bet_user.picture"
              alt=""
              class="aspect-square h-5 w-5 rounded-full"
            />
            <p class="ml-1 w-44 truncate">
              {{ decoration.last_bet_user.username }}
            </p>
          </div>
        </div>
      </div>

      <div v-if="timeLeft > 0" class="toned-bg mt-3 w-full px-3 py-3">
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
          <div class="ml-1 flex items-center">
            <img
              :src="decoration.last_bet_user.picture"
              alt=""
              class="aspect-square h-5 w-5 rounded-full"
            />
            <p class="ml-1 w-44 truncate">
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
          class="mt-3 w-full select-none rounded-full bg-[#2481cc] px-5 py-2 font-semibold text-white hover:!bg-[#1a8ad5]"
        >
          {{ $t("auction.bet") }}
        </button>
      </div>

      <div v-if="timeLeft > 0" class="toned-bg mt-3 px-3 py-3">
        <IconAlertInfo
          height="20"
          width="20"
          class="mr-0.5 inline text-gray-400"
        />
        {{ $t("auction.explain") }}
      </div>
    </div>
  </div>
</template>

<style scoped></style>
