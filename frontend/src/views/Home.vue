<script setup lang="ts">
import HomeSquadHeader from "@/components/HomeSquadHeader.vue";
import HomeUserStatsHeader from "@/components/HomeUserStatsHeader.vue";
import HomePorkSnout from "@/components/HomePorkSnout.vue";
import HomeFooterActions from "@/components/HomeFooterActions.vue";
import { ref, Ref, onMounted } from "vue";

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

onMounted(() => {
  squeezeWithRandomTimeout();
});
</script>

<template>
  <div id="container" class="flex h-screen flex-col justify-between pb-8 pt-6">
    <div class="px-3">
      <HomeSquadHeader />
      <HomeUserStatsHeader class="mt-6" />
    </div>
    <div class="select-none" ref="noseContainer">
      <HomePorkSnout />
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
/*#container {
//  background-image: url("/farm.jpg") !important;
//  background-size: cover;
//  background-position: center;
//  background-repeat: no-repeat;
//  background-attachment: fixed;
//}*/
</style>
