<script setup lang="ts">
import { ref, computed, watch } from "vue";
import { UserPublic } from "@/types.ts";
import { useUserStore, useAlertStore } from "@/store.ts";
import { useI18n } from "vue-i18n";

const userStore = useUserStore();

const alertStore = useAlertStore();
const { t } = useI18n();

const receiverTgId = ref<string | undefined>(undefined);
const amount = ref<string | undefined>(undefined);
const isSending = ref(false);

const receiverGetterTimeout = ref<number | undefined>(undefined);
const receiver = ref<UserPublic | undefined>(undefined);

const getReceiver = () => {
  fetch(import.meta.env.VITE_API_URL + `/user/${receiverTgId.value}`, {
    credentials: "include",
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error(res.statusText);
      }
      return res.json();
    })
    .then((data) => {
      receiver.value = data;
    })
    .catch((err) => {
      receiver.value = undefined;
      console.log(err);
    });
};

const validateTgID = computed(() => {
  if (receiverTgId.value === undefined) return 1;
  if (
    receiverTgId.value === "" ||
    parseInt(receiverTgId.value) === userStore.user!.uid
  )
    return -1;
  return 0;
});

const validateAmount = computed(() => {
  if (amount.value === undefined) return 1;
  if (amount.value === "" || parseInt(amount.value) <= 0) return -1;
  return 0;
});

watch(receiverTgId, () => {
  if (receiverGetterTimeout.value !== undefined) {
    clearTimeout(receiverGetterTimeout.value);
    receiverGetterTimeout.value = undefined;
  }
  receiverGetterTimeout.value = setTimeout(getReceiver, 1000);
});

const makeTransaction = () => {
  if (isSending.value) return;
  receiverTgId.value = receiverTgId.value ?? "";
  amount.value = amount.value ?? "";
  if (validateTgID.value !== 0 || validateAmount.value !== 0) {
    if (parseInt(receiverTgId.value!) === userStore.user!.uid) {
      alertStore.displayAlert(t("frens.transactions.self_error"), "error");
    }
    return;
  }
  if (receiver.value === undefined) {
    alertStore.displayAlert(t("frens.transactions.no_receiver"), "error");
    return;
  }
  if (userStore.user!.current_coins < parseInt(amount.value!)) {
    alertStore.displayAlert(t("error.no_coins"), "error");
    return;
  }
  isSending.value = true;
  fetch(import.meta.env.VITE_API_URL + "/user/transactions", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      to_user_uid: receiverTgId.value,
      amount: parseInt(amount.value!),
    }),
  })
    .then(async (res) => {
      if (res.status >= 400 && res.status < 500) {
        throw new Error((await res.json())["detail"]);
      }
      if (!res.ok) {
        throw new Error(res.statusText);
      }
      return res.json();
    })
    .then((data) => {
      isSending.value = false;
      receiverTgId.value = undefined;
      receiver.value = undefined;
      amount.value = undefined;
      userStore.transactions.unshift(data); // assuming that user will not have a lot of transactions, so unshift is fine
      userStore.user!.current_coins -= parseInt(amount.value!);
    })
    .catch((err) => {
      alertStore.displayAlert(err, "error");
      console.log(err);
    });
};
</script>

<template>
  <div class="toned-bg relative mt-2 rounded-xl p-3">
    <h3 class="text-center text-2xl font-medium">
      {{ $t("frens.transactions.title") }}
    </h3>
    <p class="mt-2 flex items-center justify-center text-lg">
      {{ $t("frens.transactions.ur_id") }}
      <span class="ml-1 select-all">{{ userStore.user?.uid }}</span>
    </p>

    <input
      class="mt-2 w-full rounded-lg border-2 px-3 py-2 outline-none"
      :style="{
        borderColor: validateTgID === -1 ? '#ff4141' : '',
      }"
      type="number"
      :placeholder="$t('frens.transactions.input_tg_id')"
      v-model="receiverTgId"
    />

    <input
      class="mt-2 w-full rounded-lg border-2 px-3 py-2 outline-none"
      :style="{
        borderColor: validateAmount === -1 ? '#ff4141' : '',
      }"
      type="number"
      :placeholder="$t('frens.transactions.input_amount')"
      v-model="amount"
    />
    <div class="mt-2 h-[38px] w-full">
      <div class="flex items-center justify-center" v-if="receiver">
        <img
          class="aspect-square h-7 rounded-full"
          :src="receiver.picture"
          alt=""
        />
        <span class="ml-2 w-full truncate">{{ receiver.username }}</span>
      </div>
    </div>

    <button
      @click="makeTransaction"
      class="w-full rounded-full bg-[#2481cc] px-5 py-2 font-semibold text-white hover:!bg-[#1a8ad5]"
    >
      {{ $t("frens.transactions.send") }}
    </button>
  </div>
</template>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Firefox */
input[type="number"] {
  -moz-appearance: textfield;
}
</style>
