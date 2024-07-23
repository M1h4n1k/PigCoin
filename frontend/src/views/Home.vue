<script setup lang="ts">
import HomeSquadHeader from "@/components/HomeSquadHeader.vue";
import HomeUserStatsHeader from "@/components/HomeUserStatsHeader.vue";
import HomePorkNose from "@/components/HomePorkNose.vue";
import HomeFooterActions from "@/components/HomeFooterActions.vue";
import { ref, Ref, onMounted } from "vue";
import { useUserStore } from "@/store";

const userStore = useUserStore();

const noseContainer: Ref<HTMLElement | null> = ref(null);

const squeezeWithRandomTimeout = () => {
  // Generate random timeout between 5 and 15 seconds (adjust as needed)
  const randomTimeout = Math.floor(Math.random() * (15000 - 5000 + 1)) + 5000;
  if (!noseContainer.value) return;
  noseContainer.value.classList.add("image-squeeze");
  setTimeout(() => {
    if (!noseContainer.value) return;
    noseContainer.value.classList.remove("image-squeeze");
  }, 500);

  // Schedule next iteration with random timeout
  setTimeout(squeezeWithRandomTimeout, randomTimeout);
};

if (userStore.autoCoins === null) {
  fetch(import.meta.env.VITE_API_URL + "/user/autoCoins", {
    credentials: "include",
  })
    .then((res) => res.json())
    .then((data) => {
      userStore.autoCoins = data;
    })
    .catch((err) => {
      console.log(err);
    });
}

const collectAutoCoins = () => {
  userStore.autoCoins = 0;
  fetch(import.meta.env.VITE_API_URL + "/user/autoCoins", {
    method: "POST",
    credentials: "include",
  })
    .then((res) => res.json())
    .then((data) => {
      userStore.user = data;
    })
    .catch((err) => {
      console.log(err);
    });
};

onMounted(() => {
  setTimeout(
    () => {
      squeezeWithRandomTimeout();
    },
    Math.floor(Math.random() * (15000 - 5000 + 1)) + 5000,
  );
});
</script>

<template>
  <div
    id="container"
    class="h-tg-screen flex flex-col justify-between pb-8 pt-2"
  >
    <div
      v-if="userStore.autoCoins !== null && userStore.autoCoins > 0"
      class="absolute left-1/2 top-1/2 z-30 flex h-48 w-80 max-w-full -translate-x-1/2 -translate-y-1/2 transform flex-col items-center justify-center rounded-xl !border-2 bg-white px-10 shadow-2xl"
    >
      <div class="text-center">
        <h3 class="text-2xl font-bold"></h3>
        <p class="flex items-center justify-center text-xl">
          {{ $t("home.offline_coins") }} {{ userStore.autoCoins }}
          {{ $t("common.coins", userStore.autoCoins) }}
        </p>
      </div>

      <button
        @click="collectAutoCoins"
        class="mt-6 w-full rounded-full border bg-[#64b5ef] py-2 font-semibold text-white"
      >
        {{ $t("home.collect") }}
      </button>
    </div>

    <div class="z-30 px-3">
      <HomeSquadHeader />
      <HomeUserStatsHeader class="mt-3" />
    </div>
    <div class="select-none" ref="noseContainer">
      <HomePorkNose />
    </div>
    <HomeFooterActions class="px-3" />
  </div>
</template>

<style scoped>
/* Used in the image-squeezer function */
.image-squeeze {
  animation: image-squeeze-animation 0.5s infinite;
}

@keyframes image-squeeze-animation {
  0% {
    transform: scale(1);
  }
  25% {
    transform: scaleY(0.95);
  }
  50% {
    transform: scale(1);
  }
  75% {
    transform: scaleY(0.95);
  }
  100% {
    transform: scale(1);
  }
}
</style>
