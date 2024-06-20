<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue";
import RatingUserCard from "@/components/RatingUserCard.vue";
import { useUserStore } from "@/store.ts";
import { openLink } from "@/utils.ts";
import RatingRowCard from "@/components/RatingUserCard.vue";
import LoadingIcon from "@/components/LoadingIcon.vue";

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

if (userStore.clubMembers.length === 0) {
  loadMembers();
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
    <div class="flex gap-4">
      <img class="h-32 w-32" :src="userStore.user!.club?.picture" alt="Club" />

      <div class="flex w-full flex-col justify-around gap-2">
        <div>
          <p class="text-center text-2xl font-semibold">
            {{ userStore.user!.club?.name }}
          </p>
          <p class="text-center">
            {{ userStore.user!.club?.members_count }}
            {{ $t("common.members", userStore.user!.club?.members_count) }}
          </p>
          <p class="text-center">
            {{ userStore.user!.club?.total_coins }}
            {{ $t("common.coins") }}
          </p>
        </div>
        <button
          @click="openLink(userStore.user!.club?.tg_link)"
          class="toned-image-bg mt-0.5 w-full cursor-pointer rounded-xl !border-2 px-4 py-2 font-medium"
        >
          {{ $t("rating.see_channel") }}
        </button>
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

      <div v-if="loading" class="flex w-full items-center justify-center p-4">
        <LoadingIcon />
      </div>

      <RatingRowCard
        v-if="userStore.user!.position_in_club! > userStore.clubMembers.length"
        class="toned-image-bg sticky bottom-0 top-0 rounded-xl p-2"
        :picture="userStore.user!.picture"
        :rating="userStore.user!.position"
        :coins="userStore.user!.total_coins"
        :name="userStore.user!.username"
        :is-you="true"
      />
    </div>
  </div>
</template>

<style scoped></style>
