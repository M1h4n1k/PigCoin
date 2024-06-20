<script setup lang="ts">
import { ref, watch, Ref, onMounted, onUnmounted } from "vue";
import RatingRowCard from "@/components/RatingUserCard.vue";
import BarnIcon from "@/components/BarnIcon.vue";
import FarmerIcon from "@/components/FarmerIcon.vue";
import PopupWindow from "@/components/PopupWindow.vue";
import { useUserStore, useRatingStore } from "@/store.ts";
import { Club, UserPublic } from "@/types.ts";
import { useRouter } from "vue-router";
import { openLink } from "@/utils.ts";
import LoadingIcon from "@/components/LoadingIcon.vue";

const router = useRouter();

const userStore = useUserStore();
const ratingStore = useRatingStore();

const activeTab = ref(0);
const league = ref(userStore.user?.league ?? 0);
const tabNames: ["users", "clubs"] = ["users", "clubs"];

const rowsContainer: Ref<Element | null> = ref(null);
const loading = ref(false);

const preloadRating = (offset = 0, limit = 20) => {
  const leagueRows = ratingStore[tabNames[activeTab.value]][league.value];

  if (leagueRows?.loaded) return;
  if (leagueRows !== undefined && offset < leagueRows.data.length) return;
  if (loading.value) return;
  loading.value = true;

  fetch(
    import.meta.env.VITE_API_URL +
      `/rating/${tabNames[activeTab.value]}?league=${league.value}&offset=${offset}&limit=${limit}`,
    {
      credentials: "include",
    },
  )
    .then((res) => res.json())
    .then((data) => {
      if (leagueRows === undefined) {
        ratingStore[tabNames[activeTab.value]][league.value] = {
          data: [],
          loaded: false,
        };
      }
      if (data.length === 0 || data.length < limit)
        ratingStore[tabNames[activeTab.value]][league.value].loaded = true;
      ratingStore[tabNames[activeTab.value]][league.value].data.push(...data);
      loading.value = false;
    })
    .catch((err) => {
      console.log(err);
    });
};

const selectedClub = ref({
  id: 0,
  name: "",
  isDisplayed: false,
} as Club & { isDisplayed: boolean });

const joinClub = (club: Club) => {
  fetch(import.meta.env.VITE_API_URL + `/clubs/${club.id}/join`, {
    method: "POST",
    credentials: "include",
  })
    .then((res) => res.json())
    .then((data) => {
      router.push("/club");
      selectedClub.value = { id: -2, name: "", isDisplayed: false } as Club & {
        isDisplayed: boolean;
      };
      userStore.user!.club = data;
      userStore.user!.club_id = data.id;
      for (const i of Array(3).keys()) {
        delete ratingStore[tabNames[activeTab.value]][i];
      }
    })
    .catch((err) => {
      console.log(err);
    });
};

const showClub = (club: Club) => {
  selectedClub.value = JSON.parse(JSON.stringify(club));
  selectedClub.value.isDisplayed = true;
};

const windowScroller = () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
    preloadRating(
      ratingStore[tabNames[activeTab.value]][league.value]?.data.length ?? 0,
    );
  }
};

onMounted(() => {
  window.addEventListener("scroll", windowScroller);
});

onUnmounted(() => {
  window.removeEventListener("scroll", windowScroller);
});

watch(league, () => preloadRating());
watch(activeTab, () => preloadRating());
preloadRating();
</script>

<template>
  <div ref="rowsContainer" class="flex flex-col items-center px-3 py-6">
    <div class="flex flex-col items-center">
      <div class="toned-bg flex w-fit cursor-pointer rounded-2xl">
        <div
          class="rounded-xl px-3 py-2 font-medium"
          :class="{
            'bg-yellow-300': activeTab === 0,
          }"
          @click="activeTab = 0"
        >
          {{ $t("rating.option.1") }}
        </div>
        <div
          class="rounded-xl px-3 py-2 font-medium"
          :class="{
            'bg-yellow-300': activeTab === 1,
          }"
          @click="activeTab = 1"
        >
          {{ $t("rating.option.2") }}
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
          <FarmerIcon
            v-if="activeTab === 0"
            class="h-24 w-24"
            :league="league"
          />
          <BarnIcon
            v-else-if="activeTab === 1"
            class="h-24 w-24"
            :league="league"
          />

          <span class="absolute mt-2 w-full text-center font-medium">
            {{ $t("rating.leagues", league) }}
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
        v-for="(row, i) in ratingStore[tabNames[activeTab]][league]?.data ?? []"
        @click="activeTab === 1 ? showClub(row as Club) : null"
        :key="i"
        class="bottom-0 top-0 rounded-xl p-2"
        :class="{
          'toned-image-bg':
            (row as UserPublic).tg_id === userStore.user?.tg_id ||
            (row as Club).id === userStore.user!.club?.id,
          'cursor-pointer': activeTab === 1,
        }"
        :style="{
          position:
            (row as UserPublic).tg_id === userStore.user?.tg_id ||
            (row as Club).id === userStore.user!.club?.id
              ? 'sticky'
              : 'static',
        }"
        :picture="row.picture"
        :rating="i + 1"
        :coins="row.total_coins"
        :name="(row as UserPublic).username ?? (row as Club).name"
        :is-you="(row as UserPublic).tg_id === userStore.user?.tg_id"
      />
      <div v-if="loading" class="flex w-full items-center justify-center p-4">
        <LoadingIcon />
      </div>

      <RatingRowCard
        v-if="
          league === userStore.user!.league &&
          activeTab === 0 &&
          ratingStore[tabNames[activeTab]][league] &&
          userStore.user!.position! >
            ratingStore[tabNames[activeTab]][league].data.length
        "
        class="toned-image-bg sticky bottom-0 top-0 rounded-xl p-2"
        :picture="userStore.user!.picture"
        :rating="userStore.user!.position"
        :coins="userStore.user!.total_coins"
        :name="userStore.user!.username"
        :is-you="true"
      />

      <div
        v-if="
          (ratingStore[tabNames[activeTab]][league]?.data ?? [1]).length === 0
        "
        class="p-5 text-center text-2xl"
      >
        {{ $t("common.no_data") }}
      </div>
    </div>

    <PopupWindow
      @close="selectedClub.isDisplayed = false"
      :style="{
        transform: selectedClub.isDisplayed
          ? 'translateY(0)'
          : 'translateY(100%)',
      }"
      :header="selectedClub.name"
    >
      <!-- picture, total coins, members count and buttons to join and see the group -->
      <div class="flex gap-4">
        <img class="h-32 w-32" :src="selectedClub?.picture" alt="Club" />

        <div class="flex w-full flex-col justify-around">
          <div>
            <p class="text-center">
              {{ selectedClub.members_count }}
              {{ $t("common.members", selectedClub.members_count) }}
            </p>
            <p class="text-center">
              {{ selectedClub?.total_coins }}
              {{ $t("common.coins") }}
            </p>
          </div>
          <div class="mt-0.5 flex w-full flex-col">
            <button
              @click="openLink(selectedClub.tg_link)"
              class="w-full rounded-xl border px-4 py-2"
            >
              {{ $t("rating.see_channel") }}
            </button>
            <button
              v-if="selectedClub.id !== userStore.user?.club_id"
              @click="joinClub(selectedClub!)"
              class="mt-2 w-full rounded-xl border px-4 py-2 font-semibold"
            >
              {{ $t("rating.join") }}
            </button>
          </div>
        </div>
      </div>
    </PopupWindow>
  </div>
</template>

<style scoped></style>
