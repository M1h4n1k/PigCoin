<script setup lang="ts">
import { ref, onMounted, onUnmounted, watchEffect } from "vue";
import RatingUserCard from "@/components/RatingUserCard.vue";
import { useUserStore } from "@/store.ts";
import { openLink, shareInviteLink } from "@/utils.ts";
import RatingRowCard from "@/components/RatingUserCard.vue";
import LoadingIcon from "@/components/LoadingIcon.vue";
import { useRouter } from "vue-router";

const router = useRouter();
const userStore = useUserStore();
const loading = ref(false);

const loadMembers = (offset = 0, limit = 20) => {
  if (userStore.clubMembersLoaded) return;
  if (loading.value) return;
  if (offset < userStore.clubMembers.length) return;
  loading.value = true;

  fetch(
    import.meta.env.VITE_API_URL +
      `/clubs/${userStore.user!.club_id}/members?offset=${offset}&limit=${limit}`,
    {
      credentials: "include",
    },
  )
    .then((res) => res.json())
    .then((data) => {
      if (data.length === 0 || data.length < limit)
        userStore.clubMembersLoaded = true;
      userStore.clubMembers.push(...data);
      loading.value = false;
    })
    .catch((err) => {
      console.log(err);
    });
};

const leaveClub = () => {
  fetch(import.meta.env.VITE_API_URL + "/clubs/leave", {
    method: "DELETE",
    credentials: "include",
  })
    .then((res) => res.json())
    .then((data) => {
      userStore.user = data;
      userStore.clubMembers = [];
      userStore.clubMembersLoaded = false;
      router.push("/");
    })
    .catch((err) => {
      console.log(err);
    });
};

if (userStore.clubMembers.length === 0 && userStore.user?.club_id) {
  loadMembers();
} else {
  watchEffect(() => {
    if (userStore.user && userStore.user.club_id) {
      loadMembers();
    }
  });
}

const windowScroller = () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 100) {
    loadMembers(userStore.clubMembers.length);
  }
};

onMounted(() => {
  window.addEventListener("scroll", windowScroller);
});

onUnmounted(() => {
  window.removeEventListener("scroll", windowScroller);
});
</script>

<template>
  <div id="container" class="flex flex-col items-center px-3 py-6">
    <div class="flex w-full gap-4">
      <img
        class="h-32 w-32 rounded-xl"
        draggable="false"
        :src="userStore.user!.club?.picture"
        alt="club"
      />

      <div class="flex flex-grow flex-col justify-around gap-2">
        <div>
          <p class="text-center text-2xl font-semibold">
            {{ userStore.user!.club?.name }}
          </p>
          <p class="text-center">
            {{ userStore.user!.club?.members_count }}
            {{ $t("common.members", userStore.user!.club?.members_count!) }}
          </p>
          <p class="text-center">
            {{ userStore.user!.club?.total_coins.toLocaleString() }}
            {{ $t("common.coins") }}
          </p>
        </div>
        <button
          @click="openLink('https://t.me/' + userStore.user!.club!.tg_tag)"
          class="toned-image-bg mt-0.5 flex w-full cursor-pointer items-center justify-center rounded-xl !border-2 px-4 py-2 font-medium"
        >
          {{ $t("club.see_channel") }}
          <svg class="ml-2" height="20px" width="20px" viewBox="0 0 100 100">
            <path
              d="M50.0 16.7L50.0 16.7L49.7 17.0Q49.0 18.3 48.7 19.7Q48.3 21.0 48.0 23.3L48.0 23.3L48.0 30.3Q30.7 31.7 20.3 42.7L20.3 42.7Q10.7 52.7 7.3 70.3L7.3 70.3L6.3 75.7L6.3 79L7.3 80.7Q9.0 83.7 12.3 83.7L12.3 83.7L13.7 83.7Q14.3 83.7 14.7 83.3L14.7 83.3L23.0 77Q33.0 69 47.3 68L47.3 68L48.0 68L48.0 74Q48.0 77 48.5 78.5Q49.0 80 50.0 81.3L50.0 81.3Q52.7 84.3 56.7 84.3L56.7 84.3L57.7 84Q59.3 84 61.3 82.7L61.3 82.7L91.3 55.0Q92.7 53.3 93.3 51.7L93.3 51.7Q94.3 49.0 93.3 46.3L93.3 46.3Q93.0 44.7 91.7 43.3L91.7 43.3L64.7 18.3L61.0 15.0Q59.3 14.0 57.7 13.7L57.7 13.7L56.7 13.7Q52.7 13.3 50.0 16.7ZM56.3 34.3L56.7 22.3L57.7 23.0L85.7 49.0L58.7 73.7L56.7 75.7L56.3 63.7Q56.3 61.7 55.2 60.5Q54.0 59.3 52.3 59.3L52.3 59.3Q30.7 59.3 16.7 71.3L16.7 71.3L15.7 72L15.7 72Q18.7 56.0 27.0 47.7L27.0 47.7Q36.3 38.7 52.3 38.7L52.3 38.7Q54.0 38.7 55.2 37.3Q56.3 36 56.3 34.3L56.3 34.3Z"
            ></path>
          </svg>
        </button>
      </div>
    </div>

    <div class="mt-2 flex w-full gap-1">
      <button
        @click="shareInviteLink('club')"
        class="toned-image-bg flex w-1/2 cursor-pointer items-center justify-center rounded-xl !border-2 px-2 py-2 font-medium"
      >
        {{ $t("club.invite") }}
        <svg
          class="img-hor-vert ml-1"
          height="25px"
          width="25px"
          viewBox="0 0 100 100"
        >
          <path
            d="M43.7 27.0L43.7 27.0Q43.7 24.3 45.0 21.8Q46.3 19.3 48.8 17.8Q51.3 16.3 54.2 16.3Q57.0 16.3 59.5 17.8Q62.0 19.3 63.3 21.8Q64.7 24.3 64.7 27.0L64.7 27.0Q64.7 31.3 61.5 34.3Q58.3 37.3 54.2 37.3Q50.0 37.3 46.8 34.3Q43.7 31.3 43.7 27.0ZM54.0 8.3L54.0 8.3Q46.3 8.3 40.8 13.8Q35.3 19.3 35.3 27.2Q35.3 35.0 40.8 40.5Q46.3 46.0 54.2 46.0Q62.0 46.0 67.5 40.5Q73.0 35.0 73.0 27.2Q73.0 19.3 67.5 13.8Q62.0 8.3 54.0 8.3ZM33.3 63.0L33.3 63.0Q42.0 58.3 54.0 58.3L54.0 58.3Q65.3 58.3 73.3 62.0L73.3 62.0Q78.7 64.7 82.3 68.7L82.3 68.7Q83.3 70 83.3 72.7Q83.3 75.3 81.3 77.3Q79.3 79.3 76.7 79.3L76.7 79.3L50.0 79.3Q48.3 79.3 47.0 80.5Q45.7 81.7 45.7 83.3Q45.7 85 47.0 86.3Q48.3 87.7 50.0 87.7L50.0 87.7L76.7 87.7Q83.0 87.3 87.3 83Q91.7 78.7 91.7 72.7Q91.7 66.7 88.3 63.0L88.3 63.0Q83.7 58.0 77.0 54.7L77.0 54.7Q67.0 50.0 54.0 50.0L54.0 50.0Q39.7 50.0 29.3 55.7L29.3 55.7Q27.7 56.7 27.3 58.3Q27.0 60.0 27.7 61.5Q28.3 63.0 30.0 63.5Q31.7 64.0 33.3 63.0ZM25.0 66.7L25.0 66.7Q26.7 66.7 27.8 67.8Q29.0 69 29.0 70.7L29.0 70.7L29.0 79L37.7 79Q39.3 79 40.5 80.3Q41.7 81.7 41.7 83.3Q41.7 85 40.5 86.2Q39.3 87.3 37.7 87.3L37.7 87.3L29.0 87.3L29.0 95.7Q29.0 97.7 27.8 98.8Q26.7 100 25.0 100Q23.3 100 22.2 98.8Q21.0 97.7 21.0 95.7L21.0 95.7L21.0 87.3L12.7 87.3Q10.7 87.3 9.5 86.2Q8.3 85 8.3 83.3Q8.3 81.7 9.5 80.3Q10.7 79 12.3 79L12.3 79L21.0 79L21.0 70.7Q21.0 69 22.2 67.8Q23.3 66.7 25.0 66.7Z"
          ></path>
        </svg>
      </button>
      <button
        @click="leaveClub"
        class="toned-image-bg flex w-1/2 cursor-pointer items-center justify-center rounded-xl !border-2 px-2 py-2 font-medium text-red-600"
      >
        {{ $t("club.leave") }}
        <svg class="ml-2" height="20px" width="20px" viewBox="0 0 100 100">
          <path
            d="M24.3 8.3L25.0 8.3L46.0 8.3Q52.7 8.3 57.7 13.2Q62.7 18.0 62.7 25.0L62.7 25.0Q62.7 26.7 61.5 27.8Q60.3 29.0 58.7 29.2Q57.0 29.3 55.7 28.2Q54.3 27.0 54.3 25.3L54.3 25.3L54.0 24.3Q54.0 21.3 51.8 19.2Q49.7 17.0 46.3 16.7L46.3 16.7L25.0 16.7Q21.7 16.7 19.3 18.8Q17.0 21.0 16.7 24.3L16.7 24.3L16.7 75Q16.7 78.3 18.8 80.7Q21.0 83 24.3 83.3L24.3 83.3L46.0 83.3Q49.0 83.3 51.5 81.2Q54.0 79 54.0 75.7L54.0 75.7L54.3 74.7Q54.3 73 55.7 71.8Q57.0 70.7 58.7 70.8Q60.3 71 61.3 72.2Q62.3 73.3 62.7 75L62.7 75Q62.7 81.7 58.0 86.5Q53.3 91.3 46.7 91.7L46.7 91.7L25.0 91.7Q18.3 91.7 13.5 87Q8.7 82.3 8.3 75.7L8.3 75.7L8.3 25.0Q8.3 18.3 13.0 13.5Q17.7 8.7 24.3 8.3L24.3 8.3ZM78.0 30.3L78.0 30.3L94.7 47.0L95.7 48.3L95.7 50.3L95.3 52.3L78.0 69.7Q76.7 70.7 75.0 70.7Q73.3 70.7 72.0 69.5Q70.7 68.3 70.7 66.7Q70.7 65 72.0 63.7L72.0 63.7L81.7 54.0L54.0 54.0Q52.7 54.0 51.5 53.0Q50.3 52.0 50.0 50.3L50.0 50.3L50.0 50.0Q50.0 48.3 51.0 47.2Q52.0 46.0 53.7 46.0L53.7 46.0L81.7 46.0L72.0 36.3Q70.7 35.0 70.7 33.3Q70.7 31.7 72.0 30.5Q73.3 29.3 75.0 29.3Q76.7 29.3 78.0 30.3Z"
            fill="currentColor"
          ></path>
        </svg>
      </button>
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

      <RatingRowCard
        v-if="userStore.user!.position_in_club! > userStore.clubMembers.length"
        class="toned-image-bg sticky bottom-0 top-0 rounded-xl p-2"
        :picture="userStore.user!.picture"
        :rating="userStore.user!.position_in_club!"
        :coins="userStore.user!.total_coins"
        :name="userStore.user!.username"
        :is-you="true"
      />

      <div v-if="loading" class="flex w-full items-center justify-center p-4">
        <LoadingIcon />
      </div>
    </div>
  </div>
</template>

<style scoped>
.img-hor-vert {
  -moz-transform: scale(-1, 1);
  -o-transform: scale(-1, 1);
  -webkit-transform: scale(-1, 1);
  transform: scale(-1, 1);
}
</style>
