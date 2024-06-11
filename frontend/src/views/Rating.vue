<script setup lang="ts">
import { ref, watch, Ref } from "vue";
import RatingRowCard from "@/components/RatingUserCard.vue";
import BarnIcon from "@/components/BarnIcon.vue";
import PopupWindow from "@/components/PopupWindow.vue";
import { useUserStore, useRatingStore } from "@/store.ts";
import { Club } from "@/types.ts";
import { useRouter } from "vue-router";

const router = useRouter();

const userStore = useUserStore();
const ratingStore = useRatingStore();

const activeTab = ref(0);
const league = ref(userStore.user?.league ?? 0);
const tabNames: ["users", "clubs"] = ["users", "clubs"];

const preloadRating = () => {
  if (ratingStore[tabNames[activeTab.value]][league.value] === undefined) {
    fetch(
      import.meta.env.VITE_API_URL +
        `/rating/${tabNames[activeTab.value]}?league=${league.value}`,
      {
        credentials: "include",
      },
    )
      .then((res) => res.json())
      .then((data) => {
        ratingStore[tabNames[activeTab.value]][league.value] = data;
      })
      .catch((err) => {
        console.log(err);
      });
  }
};

const selectedClub: Ref<Club> = ref({ id: -1, header: "" } as Club);

watch(league, preloadRating);
watch(activeTab, preloadRating);
preloadRating();

const joinClub = (club: Club) => {
  fetch(import.meta.env.VITE_API_URL + `/club/${club.id}/join`, {
    method: "POST",
    credentials: "include",
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.success) {
        userStore.user!.club = data;
        userStore.user!.club_id = data.id;
        router.push("/club");
      }
    })
    .catch((err) => {
      console.log(err);
    });
};

const showClub = (club: Club) => {
  selectedClub.value = JSON.parse(JSON.stringify(club));
};
</script>

<template>
  <div id="container" class="flex flex-col items-center px-5 py-6">
    <div class="flex flex-col items-center">
      <div class="toned-bg flex w-fit cursor-pointer rounded-2xl">
        <div
          class="rounded-xl px-3 py-2 font-medium"
          :class="{
            'bg-yellow-300': activeTab === 0,
          }"
          @click="activeTab = 0"
        >
          Swineherds
        </div>
        <div
          class="rounded-xl px-3 py-2 font-medium"
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
          class="-right-[22px] rotate-180 cursor-pointer"
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
          <BarnIcon class="h-24 w-24" :league="league" />

          <span class="absolute mt-2 w-full text-center font-medium">
            {{ league + 1 }}
          </span>
        </div>
        <svg
          class="-right-[22px] cursor-pointer"
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

    <div class="toned-bg mt-10 min-h-full w-full rounded-xl">
      <RatingRowCard
        v-for="(row, i) in ratingStore[tabNames[activeTab]][league]"
        @click="activeTab === 1 ? showClub(row) : null"
        :key="i"
        class="bottom-0 top-0 rounded-xl p-2"
        :class="{
          'toned-image-bg':
            row.tg_id === userStore.user?.tg_id ||
            row.id === userStore.user!.club?.id,
          'cursor-pointer': activeTab === 1,
        }"
        :style="{
          position:
            row.tg_id === userStore.user?.tg_id ||
            row.id === userStore.user!.club?.id
              ? 'sticky'
              : 'static',
        }"
        :picture="row.picture"
        :rating="i + 1"
        :coins="row.total_coins"
        :name="row.username ?? row.name"
        :is-you="row.tg_id === userStore.user?.tg_id"
      />
    </div>

    <PopupWindow
      @close="selectedClub.id = -1"
      :style="{
        transform: selectedClub.id > 0 ? 'translateY(0)' : 'translateY(100%)',
      }"
      :header="selectedClub?.name"
    >
      <!-- picture, total coins, members count and buttons to join and see the group -->
      <div class="flex gap-4">
        <img class="h-32 w-32" :src="selectedClub?.picture" alt="Club" />

        <div class="flex w-full flex-col justify-between">
          <div>
            <p class="">{{ selectedClub?.total_coins }} Total coins</p>
            <p class="">10 members</p>
          </div>
          <div class="mt-0.5 flex w-full flex-col">
            <button class="w-full rounded-xl border px-4 py-2">
              See group
            </button>
            <button
              @click="joinClub(selectedClub!)"
              class="mt-2 w-full rounded-xl border px-4 py-2 font-semibold"
            >
              Join
            </button>
          </div>
        </div>
      </div>
    </PopupWindow>
  </div>
</template>

<style scoped></style>
