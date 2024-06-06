<script setup lang="ts">
import { ref } from "vue";
import RatingUserCard from "@/components/RatingUserCard.vue";

const activeTab = ref("swineherds");
</script>

<template>
  <div id="container" class="flex flex-col items-center pt-6">
    <div class="flex flex-col items-center">
      <div class="flex w-fit rounded-2xl bg-gray-200">
        <div
          class="rounded-2xl px-3 py-2 font-medium"
          :class="{
            'bg-yellow-300': activeTab === 'swineherds',
          }"
          @click="activeTab = 'swineherds'"
        >
          Swineherds
        </div>
        <div
          class="rounded-2xl px-3 py-2 font-medium"
          :class="{
            'bg-yellow-300': activeTab === 'Barns',
          }"
          @click="activeTab = 'Barns'"
        >
          Barns
        </div>
      </div>
      <div class="mb-6 mt-5 flex items-center">
        <svg
          class="-right-[22px] rotate-180"
          height="70px"
          width="70px"
          viewBox="0 0 100 100"
        >
          <path
            d="M40.0 21.7L65.3 47.0Q66.7 48.3 66.7 49.8Q66.7 51.3 65.7 52.7L65.7 52.7L40.3 78Q39.3 79 37.7 79.2Q36.0 79.3 34.7 78.2Q33.3 77 33.3 75.3Q33.3 73.7 34.3 72.3L34.3 72.3L56.7 50.0L34.7 28.0Q33.3 27.0 33.3 25.3Q33.3 23.7 34.3 22.3L34.3 22.3L34.7 22.0Q35.7 21.0 37.2 20.8Q38.7 20.7 40.0 21.7L40.0 21.7Z"
          ></path>
        </svg>
        <div class="relative">
          <div class="h-24 w-24 bg-gray-200" />

          <span class="absolute mt-2 w-full text-center font-medium">
            Bronze
          </span>
        </div>
        <svg
          class="-right-[22px]"
          height="70px"
          width="70px"
          viewBox="0 0 100 100"
        >
          <path
            d="M40.0 21.7L65.3 47.0Q66.7 48.3 66.7 49.8Q66.7 51.3 65.7 52.7L65.7 52.7L40.3 78Q39.3 79 37.7 79.2Q36.0 79.3 34.7 78.2Q33.3 77 33.3 75.3Q33.3 73.7 34.3 72.3L34.3 72.3L56.7 50.0L34.7 28.0Q33.3 27.0 33.3 25.3Q33.3 23.7 34.3 22.3L34.3 22.3L34.7 22.0Q35.7 21.0 37.2 20.8Q38.7 20.7 40.0 21.7L40.0 21.7Z"
          ></path>
        </svg>
      </div>
    </div>

    <div class="mt-10 w-full bg-gray-100">
      <RatingUserCard
        class="p-2"
        v-for="i in 10"
        :key="i"
        :rating="i"
        :coins="100000 * (10 - i)"
        :name="'user' + i"
      />
    </div>
  </div>
  <div class="fixed bottom-0 w-full bg-gray-300">
    <RatingUserCard
      :is-you="true"
      rating="100k+"
      :coins="1000"
      name="Mihanik"
    />
  </div>
</template>

<style scoped></style>
