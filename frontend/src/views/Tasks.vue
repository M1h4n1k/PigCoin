<script setup lang="ts">
import { ref, onUnmounted, computed } from "vue";
import TaskCard from "@/components/TaskCard.vue";
import { useTasksStore, useAlertStore, useUserStore } from "@/store.ts";
import LoadingIcon from "@/components/LoadingIcon.vue";
import { useAdsgram } from "@/useAdsgram.ts";
import { useI18n } from "vue-i18n";

const { t } = useI18n();
const alertStore = useAlertStore();
const userStore = useUserStore();
const tasksStore = useTasksStore();
const loading = ref(tasksStore.tasks.length === 0);
const currentDate = ref(Date.now());

const timerInterval = setInterval(() => {
  currentDate.value = Date.now();
}, 1000);

onUnmounted(() => {
  clearInterval(timerInterval);
});

const { showAd } = useAdsgram({
  blockId: "2029",
  onReward: () => {
    alertStore.displayAlert(t("tasks.ad.success"), "info");
    fetch(import.meta.env.VITE_API_URL + "/tasks/ad", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        userStore.user = data;
      });
  },
  onError: (error) => {
    alertStore.displayAlert(error.description, "error");
  },
});

const showAdWrapper = () => {
  if (
    currentDate.value - Date.parse(userStore.user!.last_ad_collected) <
    60 * 72 * 1000
  ) {
    alertStore.displayAlert(t("tasks.ad.time"), "error");
    return;
  }
  showAd();
};

const timeLeft = computed(() => {
  if (!userStore.user?.last_ad_collected) return 0;
  return (
    (60 * 72 * 1000 -
      (currentDate.value - Date.parse(userStore.user!.last_ad_collected))) /
    1000
  );
});

const adTimer = () => {
  return (
    Math.round(timeLeft.value / 60 / 60)
      .toString()
      .padStart(2, "0") +
    ":" +
    Math.round((timeLeft.value / 60) % 60)
      .toString()
      .padStart(2, "0") +
    ":" +
    Math.round(timeLeft.value % 60)
      .toString()
      .padStart(2, "0")
  );
};

if (tasksStore.tasks.length === 0) {
  fetch(import.meta.env.VITE_API_URL + "/tasks/", {
    credentials: "include",
  })
    .then((res) => res.json())
    .then((data) => {
      tasksStore.tasks = data;
      loading.value = false;
    });
}
</script>

<template>
  <div class="px-3 pb-4">
    <div class="toned-bg mt-4 pb-3 text-center">
      <p class="text-7xl">
        <img
          class="inline h-14 w-14"
          draggable="false"
          src="/pigNoseCoin.svg"
          alt="🐽"
        />
      </p>
      <p class="text-4xl">
        {{ $t("tasks.earn") }}
      </p>
    </div>
    <div
      class="toned-bg mt-4 flex flex-col justify-around gap-3 rounded-xl p-5"
    >
      <TaskCard
        :id="-1"
        picture="/playAd.svg"
        :reward="500"
        type="ad"
        :completed="false"
        @click="() => showAdWrapper()"
        ><span class="text-sm text-gray-500" v-if="timeLeft > 0">{{
          adTimer()
        }}</span></TaskCard
      >
      <TaskCard
        v-for="t in tasksStore.tasks"
        :key="t.id"
        :id="t.id"
        :picture="t.picture"
        :reward="t.reward"
        :link="t.link"
        :type="t.type"
        :completed="t.completed"
      />

      <div v-if="loading" class="flex w-full items-center justify-center p-2">
        <LoadingIcon />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
