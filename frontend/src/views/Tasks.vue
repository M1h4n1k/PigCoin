<script setup lang="ts">
import { ref } from "vue";
import TaskCard from "@/components/TaskCard.vue";
import { useTasksStore } from "@/store.ts";
import LoadingIcon from "@/components/LoadingIcon.vue";

const tasksStore = useTasksStore();
const loading = ref(tasksStore.tasks.length === 0);

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
