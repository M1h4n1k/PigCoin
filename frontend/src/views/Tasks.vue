<script setup lang="ts">
import { ref } from "vue";
import TaskCard from "@/components/TaskCard.vue";
import { useTasksStore, useAlertStore, useUserStore } from "@/store.ts";
import LoadingIcon from "@/components/LoadingIcon.vue";
import { useAdsgram } from "@/useAdsgram.ts";

const alertStore = useAlertStore();
const userStore = useUserStore();
const tasksStore = useTasksStore();
const loading = ref(tasksStore.tasks.length === 0);

const { showAd } = useAdsgram({
  blockId: "2029",
  onReward: () => {
    alertStore.displayAlert("You earned 500 coins!", "info");
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
  if (!userStore.user!.can_collect_ad) {
    alertStore.displayAlert("You can watch an ad every 1.2 hours", "error");
    return;
  }
  showAd();
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
        @click="showAdWrapper"
      />
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
