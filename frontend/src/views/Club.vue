<script setup lang="ts">
import RatingUserCard from "@/components/RatingUserCard.vue";
import { useUserStore } from "@/store.ts";

const userStore = useUserStore();

if (userStore.clubMembers.length === 0) {
  fetch(
    import.meta.env.VITE_API_URL + `/clubs/${userStore.user!.club_id}/members`,
    {
      credentials: "include",
    },
  )
    .then((res) => res.json())
    .then((data) => {
      userStore.clubMembers = data;
    })
    .catch((err) => {
      console.log(err);
    });
}
</script>

<template>
  <div id="container" class="flex flex-col items-center px-5 py-6">
    <div class="mt-5 flex flex-col items-center">
      <img class="h-28 w-28" :src="userStore.user!.club?.picture" alt="" />

      <div class="relative cursor-pointer">
        <div>
          <p class="mt-2 text-center text-xl font-medium">
            {{ userStore.user!.club?.name }}
          </p>
          <p class="text-center text-sm">
            {{ userStore.clubMembers.length }} members
          </p>
        </div>
        <svg
          class="absolute -right-[25px] top-1/2"
          height="20px"
          width="20px"
          viewBox="0 0 100 100"
        >
          <path
            d="M40.0 21.7L65.3 47.0Q66.7 48.3 66.7 49.8Q66.7 51.3 65.7 52.7L65.7 52.7L40.3 78Q39.3 79 37.7 79.2Q36.0 79.3 34.7 78.2Q33.3 77 33.3 75.3Q33.3 73.7 34.3 72.3L34.3 72.3L56.7 50.0L34.7 28.0Q33.3 27.0 33.3 25.3Q33.3 23.7 34.3 22.3L34.3 22.3L34.7 22.0Q35.7 21.0 37.2 20.8Q38.7 20.7 40.0 21.7L40.0 21.7Z"
          ></path>
        </svg>
      </div>
    </div>

    <div class="toned-bg mt-6 min-h-full w-full rounded-xl">
      <RatingUserCard
        class="bottom-0 top-0 rounded-xl p-2"
        :class="{
          'toned-image-bg': row.tg_id === userStore.user?.tg_id,
        }"
        :style="{
          position: row.tg_id === userStore.user?.tg_id ? 'sticky' : 'static',
        }"
        v-for="(row, i) in userStore.clubMembers"
        :key="i"
        :picture="row.picture"
        :rating="i + 1"
        :coins="row.total_coins"
        :name="row.username"
        :is-you="row.tg_id === userStore.user?.tg_id"
      />
    </div>
  </div>
</template>

<style scoped></style>
