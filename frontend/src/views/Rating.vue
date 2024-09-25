<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted } from "vue";
import RatingRowCard from "@/components/RatingUserCard.vue";
import BarnIcon from "@/components/BarnIcon.vue";
import FarmerIcon from "@/components/FarmerIcon.vue";
import PopupWindow from "@/components/PopupWindow.vue";
import { useUserStore, useRatingStore } from "@/store.ts";
import { Club, UserPublic } from "@/types.ts";
import { useRouter } from "vue-router";
import { openLink } from "@/utils.ts";
import LoadingIcon from "@/components/LoadingIcon.vue";
import IconArrowRight from "@/components/IconArrowRight.vue";
import IconOpenLink from "@/components/IconOpenLink.vue";

const router = useRouter();

const userStore = useUserStore();
const ratingStore = useRatingStore();

const container = ref<HTMLElement | null>(null);

const activeTab = ref(0);
const league = ref(userStore.user?.league ?? 0);
const tabNames: ["users", "clubs"] = ["users", "clubs"];

const loading = ref(false);

const preloadRating = (offset = 0, limit = 20) => {
  const leagueRows = ratingStore[tabNames[activeTab.value]][league.value];

  if (leagueRows?.loaded) return;
  if (leagueRows !== undefined && offset < leagueRows.data.length) return;
  if (loading.value) return;
  loading.value = true;
  const tabName = tabNames[activeTab.value];
  const leagueValue = league.value;

  fetch(
    import.meta.env.VITE_API_URL +
      `/rating/${tabName}?league=${leagueValue}&offset=${offset}&limit=${limit}`,
    {
      credentials: "include",
    },
  )
    .then((res) => res.json())
    .then((data) => {
      if (leagueRows === undefined) {
        ratingStore[tabName][leagueValue] = {
          data: [],
          loaded: false,
        };
      }
      if (data.length === 0 || data.length < limit)
        ratingStore[tabName][leagueValue].loaded = true;
      ratingStore[tabName][leagueValue].data.push(...data);
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
  if (
    document.body.scrollTop + window.innerHeight >=
    container.value!.clientHeight - 100
  ) {
    preloadRating(
      ratingStore[tabNames[activeTab.value]][league.value]?.data.length ?? 0,
    );
  }
};

onMounted(() => {
  document.body.addEventListener("scroll", windowScroller);
});

onUnmounted(() => {
  document.body.removeEventListener("scroll", windowScroller);
});

watch(league, () => preloadRating());
watch(activeTab, () => preloadRating());
preloadRating();
</script>

<template>
  <div ref="container" class="flex select-none flex-col items-center px-3 py-6">
    <div class="flex flex-col items-center">
      <div class="toned-bg flex w-fit cursor-pointer rounded-2xl">
        <div
          class="rounded-xl px-3 py-2 font-medium"
          :class="{
            'toned-image-bg': activeTab === 0,
          }"
          @click="activeTab = 0"
        >
          {{ $t("rating.option.1") }}
        </div>
        <div
          class="rounded-xl px-3 py-2 font-medium"
          :class="{
            'toned-image-bg': activeTab === 1,
          }"
          @click="activeTab = 1"
        >
          {{ $t("rating.option.2") }}
        </div>
      </div>
      <div class="mb-6 mt-5 flex items-center">
        <IconArrowRight
          height="70px"
          width="70px"
          @click="league = (league - 1 + 3) % 3"
          class="-right-[22px] rotate-180"
        />
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
        <IconArrowRight
          height="70px"
          width="70px"
          @click="league = (league + 1) % 3"
          class="-right-[22px]"
        />
      </div>
    </div>

    <RouterLink
      v-if="activeTab === 1"
      to="/createClub"
      class="toned-bg mt-6 flex h-14 w-full cursor-pointer items-center justify-start rounded-xl px-5 py-2"
    >
      <svg class="mr-2" height="30px" width="30px" viewBox="0 0 100 100">
        <path
          d="M25.0 29.0L25.0 29.0Q25.0 27.0 26.2 25.0Q27.3 23.0 29.2 21.8Q31.0 20.7 33.3 20.7Q35.7 20.7 37.5 21.8Q39.3 23.0 40.5 25.0Q41.7 27.0 41.7 29.0L41.7 29.0Q41.7 32.7 39.2 35.0Q36.7 37.3 33.3 37.3Q30.0 37.3 27.5 35.0Q25.0 32.7 25.0 29.0ZM33.3 12.3L33.3 12.3Q26.3 12.3 21.5 17.3Q16.7 22.3 16.7 29.2Q16.7 36 21.5 40.8Q26.3 45.7 33.3 45.7Q40.3 45.7 45.2 40.8Q50.0 36 50.0 29.2Q50.0 22.3 45.2 17.3Q40.3 12.3 33.3 12.3ZM9.7 66.3L9.7 66.3Q13.0 63.3 17.7 61.3L17.7 61.3Q24.3 58.3 33.3 58.3Q42.3 58.3 49.0 61.3L49.0 61.3Q53.7 63.3 57.0 66.3L57.0 66.3Q58.3 67.7 58.3 71L58.3 71Q58.3 72.7 57.2 73.8Q56.0 75 54.3 75L54.3 75L12.3 75Q10.7 75 9.5 73.8Q8.3 72.7 8.3 71L8.3 71Q8.3 67.7 9.7 66.3ZM33.3 50.0L33.3 50.0Q22.7 50.0 14.3 53.7L14.3 53.7Q8.3 56.0 4.2 60.2Q0 64.3 0 71L0 71Q0 76 3.7 79.7Q7.3 83.3 12.3 83.3L12.3 83.3L54.3 83.3Q59.3 83.3 63.0 79.7Q66.7 76 66.7 71L66.7 71Q66.7 64.3 62.5 60.2Q58.3 56.0 52.3 53.7L52.3 53.7Q44.0 50.0 33.3 50.0ZM68.7 57.7L68.7 57.7Q68.7 56.0 70.0 54.8Q71.3 53.7 73.0 53.7L73.0 53.7Q81.3 54.0 88.0 57.0L88.0 57.0Q93.0 59.3 96.5 62.8Q100.0 66.3 100.0 72L100.0 72Q100.0 76.7 96.7 80Q93.3 83.3 88.7 83.3L88.7 83.3L75.0 83.3Q73.3 83.3 72.2 82.2Q71.0 81 71.0 79.2Q71.0 77.3 72.2 76.2Q73.3 75 75.0 75L75.0 75L88.7 75Q90.0 75 90.8 74.2Q91.7 73.3 91.7 72L91.7 72Q91.7 69.7 90.7 68.7L90.7 68.7Q84.3 62.3 72.7 62.0L72.7 62.0Q71.0 62.0 69.8 60.7Q68.7 59.3 68.7 57.7ZM64.7 35.3L64.7 35.3Q64.7 33.7 65.5 32.2Q66.3 30.7 67.7 29.8Q69.0 29.0 70.8 29.0Q72.7 29.0 74.0 29.8Q75.3 30.7 76.2 32.2Q77.0 33.7 77.0 35.3L77.0 35.3Q77.0 38.0 75.2 39.8Q73.3 41.7 70.8 41.7Q68.3 41.7 66.5 39.8Q64.7 38.0 64.7 35.3ZM71.0 21.0L71.0 21.0Q64.7 21.0 60.5 25.2Q56.3 29.3 56.3 35.3Q56.3 41.3 60.5 45.7Q64.7 50.0 70.8 50.0Q77.0 50.0 81.2 45.7Q85.3 41.3 85.3 35.3Q85.3 29.3 81.2 25.2Q77.0 21.0 71.0 21.0Z"
        ></path>
      </svg>
      <span class="text-lg">{{ $t("club.create") }}</span>
    </RouterLink>

    <div class="toned-bg mt-3 min-h-full w-full rounded-xl">
      <RatingRowCard
        v-for="(row, i) in ratingStore[tabNames[activeTab]][league]?.data ?? []"
        @click="activeTab === 1 ? showClub(row as Club) : null"
        :key="i"
        class="bottom-0 top-0 rounded-xl p-2"
        :class="{
          'toned-image-bg':
            (row as UserPublic).tg_id === userStore.user?.tg_id ||
            (userStore.user!.club &&
              (row as Club).id === userStore.user!.club.id),
          'cursor-pointer': activeTab === 1,
        }"
        :style="{
          position:
            (row as UserPublic).tg_id === userStore.user?.tg_id ||
            (userStore.user!.club &&
              (row as Club).id === userStore.user!.club.id)
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
        :rating="userStore.user!.position!"
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
      <div class="flex items-center gap-4">
        <img
          class="h-32 w-32 rounded-xl"
          :src="selectedClub?.picture"
          alt="Club"
        />

        <div class="flex flex-grow flex-col justify-around">
          <div>
            <p class="text-center">
              {{ selectedClub.members_count }}
              {{ $t("common.members", selectedClub.members_count) }}
            </p>
            <p class="text-center">
              {{ selectedClub?.total_coins?.toLocaleString() }}
              {{ $t("common.coins") }}
            </p>
          </div>
          <div class="mt-0.5 flex w-full flex-col">
            <button
              @click="openLink('https://t.me/' + selectedClub.tg_tag)"
              class="flex w-full items-center justify-center rounded-xl border px-4 py-2"
            >
              {{ $t("club.see_channel") }}
              <IconOpenLink class="ml-2" height="20px" width="20px" />
            </button>
            <button
              v-if="selectedClub.id !== userStore.user?.club_id"
              @click="joinClub(selectedClub!)"
              class="mt-2 w-full rounded-xl border px-4 py-2 font-semibold"
            >
              {{ $t("club.join") }}
            </button>
          </div>
        </div>
      </div>
    </PopupWindow>
  </div>
</template>

<style scoped></style>
