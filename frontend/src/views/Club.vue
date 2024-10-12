<script setup lang="ts">
import { ref, watchEffect } from "vue";
import RatingUserCard from "@/components/RatingUserCard.vue";
import RatingRowCard from "@/components/RatingUserCard.vue";
import { useUserStore } from "@/store.ts";
import { openLink, shareInviteLink } from "@/utils.ts";
import LoadingIcon from "@/components/LoadingIcon.vue";
import { useRouter } from "vue-router";
import IconLeave from "@/components/IconLeave.vue";
import IconInvite from "@/components/IconInvite.vue";
import IconOpenLink from "@/components/IconOpenLink.vue";
import { vInfiniteScroll } from "@/directives";

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
</script>

<template>
  <div
    v-infinite-scroll="() => loadMembers(userStore.clubMembers.length)"
    class="flex flex-col items-center px-3 py-6"
  >
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
            {{ $t("common.coins", userStore.user!.club?.total_coins!) }}
          </p>
        </div>
        <button
          @click="openLink('https://t.me/' + userStore.user!.club!.tg_tag)"
          class="toned-image-bg mt-0.5 flex w-full cursor-pointer items-center justify-center rounded-xl !border-2 px-4 py-2 font-medium"
        >
          {{ $t("club.see_channel") }}
          <IconOpenLink class="ml-2" height="20px" width="20px" />
        </button>
      </div>
    </div>

    <div class="mt-2 flex w-full gap-1">
      <button
        @click="shareInviteLink('club')"
        class="toned-image-bg flex w-1/2 cursor-pointer items-center justify-center rounded-xl !border-2 px-2 py-2 font-medium"
      >
        {{ $t("club.invite") }}
        <IconInvite class="ml-1" height="25px" width="25px" />
      </button>
      <button
        @click="leaveClub"
        class="toned-image-bg flex w-1/2 cursor-pointer items-center justify-center rounded-xl !border-2 px-2 py-2 font-medium text-red-600"
      >
        {{ $t("club.leave") }}
        <IconLeave class="ml-2" height="20px" width="20px" />
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
