<script setup lang="ts">
import { ref, watch } from "vue";
import RatingUserCard from "@/components/RatingUserCard.vue";
import { useUserStore, useRatingStore } from "@/store.ts";

const userStore = useUserStore();
const ratingStore = useRatingStore();

const activeTab = ref(0);
const league = ref(userStore.user?.league ?? 0);

const preloadRating = () => {
  const tabNames = ["users", "clubs"];
  if (ratingStore.userRating[league.value] === undefined) {
    fetch(
      import.meta.env.VITE_API_URL +
        `/rating/${tabNames[activeTab.value]}?league=${league.value}`,
      {
        credentials: "include",
      },
    )
      .then((res) => res.json())
      .then((data) => {
        ratingStore.userRating[league.value] = data;
      })
      .catch((err) => {
        console.log(err);
      });
  }
};

watch(league, preloadRating);
watch(activeTab, preloadRating);
preloadRating();
</script>

<template>
  <div id="container" class="flex flex-col items-center px-5 pt-6">
    <div class="flex flex-col items-center">
      <div class="flex w-fit rounded-2xl bg-gray-200">
        <div
          class="rounded-2xl px-3 py-2 font-medium"
          :class="{
            'bg-yellow-300': activeTab === 0,
          }"
          @click="activeTab = 0"
        >
          Swineherds
        </div>
        <div
          class="rounded-2xl px-3 py-2 font-medium"
          :class="{
            'bg-yellow-300': activeTab === 1,
          }"
          @click="activeTab = 1"
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
          @click="league = (league - 1 + 3) % 3"
        >
          <path
            d="M40.0 21.7L65.3 47.0Q66.7 48.3 66.7 49.8Q66.7 51.3 65.7 52.7L65.7 52.7L40.3 78Q39.3 79 37.7 79.2Q36.0 79.3 34.7 78.2Q33.3 77 33.3 75.3Q33.3 73.7 34.3 72.3L34.3 72.3L56.7 50.0L34.7 28.0Q33.3 27.0 33.3 25.3Q33.3 23.7 34.3 22.3L34.3 22.3L34.7 22.0Q35.7 21.0 37.2 20.8Q38.7 20.7 40.0 21.7L40.0 21.7Z"
          ></path>
        </svg>
        <div class="relative">
          <div class="h-24 w-24 bg-gray-200" />

          <span class="absolute mt-2 w-full text-center font-medium">
            {{ league }}
          </span>
        </div>
        <svg
          class="-right-[22px]"
          height="70px"
          width="70px"
          viewBox="0 0 100 100"
          @click="league = (league + 1) % 3"
        >
          <path
            d="M40.0 21.7L65.3 47.0Q66.7 48.3 66.7 49.8Q66.7 51.3 65.7 52.7L65.7 52.7L40.3 78Q39.3 79 37.7 79.2Q36.0 79.3 34.7 78.2Q33.3 77 33.3 75.3Q33.3 73.7 34.3 72.3L34.3 72.3L56.7 50.0L34.7 28.0Q33.3 27.0 33.3 25.3Q33.3 23.7 34.3 22.3L34.3 22.3L34.7 22.0Q35.7 21.0 37.2 20.8Q38.7 20.7 40.0 21.7L40.0 21.7Z"
          ></path>
        </svg>
      </div>
    </div>

    <div class="mt-10 w-full rounded-xl bg-gray-200">
      <RatingUserCard
        class="p-2"
        v-for="(u, i) in ratingStore.userRating[league]"
        :key="i"
        :picture="u.picture"
        :rating="i + 1"
        :coins="u.total_coins"
        :name="u.username"
      />
    </div>
  </div>
  <div class="fixed bottom-0 w-full px-5">
    <div class="w-full bg-gray-300">
      <RatingUserCard
        :is-you="true"
        rating="100k+"
        :coins="userStore.user?.total_coins"
        :picture="userStore.user?.picture"
        :name="userStore.user?.username"
      />
    </div>
  </div>
</template>

<style scoped></style>
