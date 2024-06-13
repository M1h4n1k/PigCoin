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
            {{ userStore.user!.club!.name }}
          </p>
          <div>
            <span class="text-center text-sm">
              {{ userStore.clubMembers.length }}
              {{ $t("common.members", userStore.user!.club!.members_count) }}
            </span>
            <span class="ml-1 mr-2 text-xl font-semibold">·</span>
            <span class="text-center text-sm">
              {{ userStore.user!.club!.total_coins }}
              {{ $t("common.coins", userStore.user!.club!.total_coins) }}
            </span>
          </div>
        </div>
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
