<script setup lang="ts">
import TaskCard from "@/components/TaskCard.vue";
import { Ref, ref } from "vue";
import { Task } from "@/types";

const tasks: Ref<Task[]> = ref([]);

fetch(import.meta.env.VITE_API_URL + "/tasks/", {
  credentials: "include",
})
  .then((res) => res.json())
  .then((data) => {
    tasks.value = data;
  });
</script>

<template>
  <div class="px-5">
    <div class="mt-4 text-center">
      <p class="text-7xl">🐽</p>
      <p class="text-4xl">Earn more coins</p>
    </div>
    <div class="mt-8 flex flex-col justify-around gap-4 rounded-xl border p-5">
      <TaskCard
        v-for="t in tasks"
        :key="t"
        :picture="t.picture"
        :title="t.title"
        :reward="t.reward"
      />
    </div>
  </div>
</template>

<style scoped></style>
