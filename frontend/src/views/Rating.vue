<script setup lang="ts">
import { ref, watch } from "vue";
import RatingRowCard from "@/components/RatingUserCard.vue";
import LeagueBarn from "@/components/LeagueBarn.vue";
import LeagueFarmer from "@/components/LeagueFarmer.vue";
import PopupWindow from "@/components/PopupWindow.vue";
import { useRatingStore, useUserStore } from "@/store.ts";
import { Club, UserPublic } from "@/types.ts";
import { useRouter } from "vue-router";
import { openLink } from "@/utils.ts";
import { vInfiniteScroll } from "@/directives";
import LoadingIcon from "@/components/LoadingIcon.vue";
import IconArrowRight from "@/components/IconArrowRight.vue";
import IconOpenLink from "@/components/IconOpenLink.vue";
import IconPeople from "@/components/IconPeople.vue";
import InputSwitch from "@/components/InputSwitch.vue";

const router = useRouter();

const userStore = useUserStore();
const ratingStore = useRatingStore();

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

watch(league, () => preloadRating());
watch(activeTab, () => preloadRating());
preloadRating();
</script>

<template>
  <div
    v-infinite-scroll="
      () =>
        preloadRating(
          ratingStore[tabNames[activeTab]][league]?.data.length ?? 0,
        )
    "
    class="flex select-none flex-col items-center px-3 py-6"
  >
    <div class="flex flex-col items-center">
      <InputSwitch
        v-model:active-tab="activeTab"
        :options="[$t('rating.option.1'), $t('rating.option.2')]"
      />
      <div class="mb-6 mt-5 flex items-center">
        <IconArrowRight
          height="70px"
          width="70px"
          @click="league = (league - 1 + 4) % 4"
          class="-right-[22px] rotate-180"
        />
        <div class="relative">
          <LeagueFarmer
            v-if="activeTab === 0"
            class="h-24 w-24"
            :league="league"
          />
          <LeagueBarn
            v-else-if="activeTab === 1"
            class="h-24 w-24"
            :league="league"
          />

          <span class="absolute mt-2 w-full text-center font-medium">
            {{ $t("rating.league." + league) }}
          </span>
        </div>
        <IconArrowRight
          height="70px"
          width="70px"
          @click="league = (league + 1) % 4"
          class="-right-[22px]"
        />
      </div>
    </div>

    <RouterLink
      v-if="activeTab === 1"
      to="/createClub"
      class="toned-bg mt-6 flex h-14 w-full cursor-pointer items-center justify-start rounded-xl px-5 py-2"
    >
      <IconPeople class="mr-2" height="30px" width="30px" />
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
            (row as UserPublic).uid === userStore.user?.uid ||
            (userStore.user!.club &&
              (row as Club).id === userStore.user!.club.id),
          'cursor-pointer': activeTab === 1,
        }"
        :style="{
          position:
            (row as UserPublic).uid === userStore.user?.uid ||
            (userStore.user!.club &&
              (row as Club).id === userStore.user!.club.id)
              ? 'sticky'
              : 'static',
        }"
        :picture="row.picture"
        :rating="i + 1"
        :coins="row.total_coins"
        :name="(row as UserPublic).username ?? (row as Club).name"
        :decoration-src="
          (row as UserPublic).decorations?.length > 0
            ? (row as UserPublic).decorations[0].picture
            : undefined
        "
        :is-you="(row as UserPublic).uid === userStore.user?.uid"
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
        :decoration-src="
          userStore.user!.decorations.length > 0
            ? userStore.user!.decorations[0].picture
            : undefined
        "
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
              @touchend.stop
              @touchstart.stop
              @click="openLink('https://t.me/' + selectedClub.tg_tag)"
              class="flex w-full items-center justify-center rounded-xl border px-4 py-2"
            >
              {{ $t("club.see_channel") }}
              <IconOpenLink class="ml-2" height="20px" width="20px" />
            </button>
            <button
              v-if="selectedClub.id !== userStore.user?.club_id"
              @touchend.stop
              @touchstart.stop
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
