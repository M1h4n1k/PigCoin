<script setup lang="ts">
import TaskCard from "@/components/TaskCard.vue";
import { Ref, ref } from "vue";
import { Task } from "@/types";
import { useTasksStore } from "@/store.ts";

const tasksStore = useTasksStore();

fetch(import.meta.env.VITE_API_URL + "/tasks/", {
  credentials: "include",
})
  .then((res) => res.json())
  .then((data) => {
    tasksStore.tasks = data;
  });
</script>

<template>
  <div class="px-5">
    <div class="toned-bg mt-4 pb-3 text-center">
      <p class="text-7xl">
        <img class="inline h-14 w-14" src="/pigNoseCoin.svg" alt="🐽" />
      </p>
      <p class="text-4xl">
        {{ $t("tasks.earn") }}
      </p>
    </div>
    <div
      class="toned-bg mt-8 flex flex-col justify-around gap-4 rounded-xl p-5"
    >
      <TaskCard
        v-for="t in tasksStore.tasks"
        :key="t"
        :picture="t.picture"
        :reward="t.reward"
        :type="t.type"
        :completed="t.completed"
      />
    </div>
  </div>
</template>

<style scoped></style>
