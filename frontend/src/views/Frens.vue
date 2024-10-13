<script setup lang="ts">
import { ref, watch } from "vue";
import RatingUserCard from "@/components/RatingUserCard.vue";
import { useUserStore } from "@/store";
import LoadingIcon from "@/components/LoadingIcon.vue";
import { vInfiniteScroll } from "@/directives.ts";
import InputSwitch from "@/components/InputSwitch.vue";
import FrensInviteHeader from "@/components/FrensInviteHeader.vue";
import FrensMakeTransaction from "@/components/FrensMakeTransaction.vue";

const userStore = useUserStore();

const loading = ref(false);
const isReferralFullyLoaded = ref(false);
const isTransactionsFullyLoaded = ref(false);

const activeTab = ref(0);

const loadReferrals = (offset = 0, limit = 20) => {
  if (loading.value || isReferralFullyLoaded.value) return;
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
      if (data.length === 0 || data.length < limit)
        isReferralFullyLoaded.value = true;
      userStore.referrals.push(...data);
      loading.value = false;
    })
    .catch((err) => {
      console.log(err);
    });
};

const loadTransactions = (offset = 0, limit = 20) => {
  if (loading.value || isTransactionsFullyLoaded.value) return;
  loading.value = true;

  fetch(
    import.meta.env.VITE_API_URL +
      `/user/transactions?offset=${offset}&limit=${limit}`,
    {
      credentials: "include",
    },
  )
    .then((res) => res.json())
    .then((data) => {
      if (data.length === 0 || data.length < limit)
        isTransactionsFullyLoaded.value = true;
      userStore.transactions.push(...data);
      loading.value = false;
    })
    .catch((err) => {
      console.log(err);
    });
};

watch(
  activeTab,
  () => {
    if (activeTab.value === 0) {
      if (userStore.referrals.length === 0) loadReferrals();
    } else {
      if (userStore.transactions.length === 0) loadTransactions();
    }
  },
  { immediate: true },
);

const formatDate = (date: number) => {
  const d = new Date(date * 1000);
  return d.toLocaleString(Telegram.WebApp.initDataUnsafe.user!.language_code, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "numeric",
  });
};
</script>

<template>
  <div class="px-3 py-2 pb-4">
    <FrensInviteHeader v-if="activeTab === 0" />
    <FrensMakeTransaction v-else />

    <InputSwitch
      class="mx-auto mt-7"
      :options="[$t('frens.options.0'), $t('frens.options.1')]"
      v-model:active-tab="activeTab"
    />

    <div
      v-infinite-scroll="
        () => {
          if (activeTab === 0) loadReferrals(userStore.referrals.length);
          else loadTransactions(userStore.transactions.length);
        }
      "
      class="toned-bg mt-2 w-full rounded-xl py-3"
    >
      <h3 class="px-5 text-start text-2xl font-medium">
        {{ $t(`frens.options.${activeTab}`) }}
      </h3>
      <div v-if="activeTab === 0">
        <RatingUserCard
          v-for="(referral, ix) in userStore.referrals"
          :key="ix"
          :picture="referral.picture"
          :rating="ix + 1"
          :coins="referral.total_coins"
          :name="referral.username"
        />
      </div>
      <div v-else>
        <div
          v-for="transaction in userStore.transactions"
          :key="transaction.created_at"
          class="relative flex items-center px-4 py-2"
        >
          <div class="flex items-center">
            <img
              class="h-7 w-7 rounded-full"
              draggable="false"
              alt=""
              :src="
                transaction.from_user.uid === userStore.user!.uid
                  ? transaction.to_user.picture
                  : transaction.from_user.picture
              "
            />
            <div
              class="ml-2 max-w-36 flex-col items-center justify-center overflow-x-clip"
            >
              <p class="truncate font-semibold">
                {{
                  transaction.from_user.uid === userStore.user!.uid
                    ? transaction.to_user.username
                    : transaction.from_user.username
                }}
              </p>
              <p class="text-gray-600">
                {{ formatDate(transaction.created_at) }}
              </p>
            </div>
          </div>
          <div class="ml-auto">
            <p
              class="out flex items-center text-lg font-medium"
              :class="[
                transaction.from_user.uid === userStore.user!.uid
                  ? 'outgoing'
                  : 'incoming',
              ]"
            >
              {{ transaction.amount.toLocaleString() }}
              <img
                class="ml-1.5 h-3 w-3"
                src="/pigNoseCoin.svg"
                alt="🐽"
                loading="lazy"
              />
            </p>
          </div>
        </div>
      </div>

      <div v-if="loading" class="flex w-full items-center justify-center p-2">
        <LoadingIcon />
      </div>
      <div
        v-if="
          userStore[activeTab === 0 ? 'referrals' : 'transactions'].length ===
            0 && !loading
        "
        class="block w-full text-center text-lg"
      >
        {{ $t("common.no_data") }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.incoming {
  color: green;
}
.outgoing {
  color: red;
}
.outgoing::before {
  content: "-";
}
.incoming::before {
  content: "+";
}
</style>
