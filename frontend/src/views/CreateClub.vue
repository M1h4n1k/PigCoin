<script setup lang="ts">
import { ref, computed } from "vue";
import { useUserStore, useAlertStore } from "@/store";
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import LoadingIcon from "@/components/LoadingIcon.vue";

const { t } = useI18n();
const router = useRouter();

const userStore = useUserStore();
const alertStore = useAlertStore();
const channelLink = ref("");

const validateChannelLink = computed(() => {
  if (channelLink.value === "") {
    return -1;
  }
  const banWords = ["https://", "http://", "t.me/", "@"];
  let channelTag = channelLink.value.trim().toLowerCase();
  for (const word of banWords) {
    channelTag = channelTag.replace(word, "");
  }
  console.log(channelTag);
  // regex [0-9a-z_]+
  if (/[^0-9a-z_]/.test(channelTag)) {
    return 1;
  }
  return 0;
});

const createClub = () => {
  if (validateChannelLink.value !== 0) {
    alertStore.displayAlert(t("club.create.invalid"), "error");
  }
  fetch(import.meta.env.VITE_API_URL + "/clubs/", {
    method: "POST",
    credentials: "include",
    body: channelLink.value,
  })
    .then((res) => {
      if (!res.ok) {
        throw new Error(res.statusText);
      }
      return res.json();
    })
    .then((data) => {
      userStore.user = data;
      router.push("/club");
    })
    .catch((err) => {
      alertStore.displayAlert(err, "error");
    });
};
</script>

<template>
  <div class="px-3 py-2 pb-4">
    <div class="toned-bg mt-2 space-y-4 rounded-xl p-3">
      <h3 class="text-center text-2xl font-medium">
        {{ $t("club.create.title") }}
      </h3>
      <div class="flex items-center">
        <img height="50" width="50" src="/trophy.png" alt="" />
        <div class="ml-4">
          <p class="text-lg font-medium">{{ $t("club.create.compete") }}</p>
        </div>
      </div>

      <div class="flex items-center">
        <img height="50" width="50" src="/gift.png" alt="" />
        <div class="ml-4">
          <p class="text-lg font-medium leading-5">
            {{ $t("club.create.prizes") }}
          </p>
        </div>
      </div>
    </div>

    <input
      class="mt-4 w-full rounded-lg border-2 px-3 py-2 outline-none"
      :style="{
        borderColor: validateChannelLink === 1 ? '#ff4141' : '',
      }"
      type="text"
      :placeholder="$t('club.create.input_placeholder')"
      v-model="channelLink"
    />

    <button
      @click="createClub"
      class="mt-4 w-full rounded-full bg-[#2481cc] px-5 py-2 font-semibold text-white hover:!bg-[#1a8ad5]"
    >
      {{ $t("club.create.button") }}
    </button>
  </div>
</template>

<style scoped></style>
