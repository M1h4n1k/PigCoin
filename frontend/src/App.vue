<script setup lang="ts">
import { onUnmounted, ref } from "vue";
import { useUserStore, useAlertStore } from "@/store";
import BgCloud from "@/components/BgCloud.vue";

const userStore = useUserStore();
const alertStore = useAlertStore();
const clouds = ref<{ id: number; top: string }[]>([]);

const refillEnergy = () => {
  userStore.user!.current_energy = Math.min(
    userStore.user!.max_energy,
    userStore.user!.current_energy + userStore.user!.refill_rate,
  );
};

const refillInterval = setInterval(() => refillEnergy(), 1000);
onUnmounted(() => clearInterval(refillInterval));

const spawnCloud = () => {
  if (clouds.value.length === 10) clearInterval(spawnCloudInterval);
  const cloud = {
    id: 1 + Math.floor(Math.random() * 9),
    top: Math.random() * 200 + "px",
  };
  clouds.value.push(cloud);
};

spawnCloud();
const spawnCloudInterval = setInterval(() => spawnCloud(), 5000);
</script>

<template>
  <div
    class="pointer-events-none fixed top-4 z-50 flex w-full items-center justify-center px-2 opacity-0 transition-opacity duration-300"
    :class="{
      '!opacity-100': alertStore.isDisplayed,
    }"
  >
    <div
      class="flex h-[45px] w-full select-none items-center rounded-xl bg-gray-800"
    >
      <svg
        height="20"
        width="20"
        class="ml-[15px]"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 189.9 189.9"
      >
        <path
          fill="#fff"
          d="m94.95,0C42.51,0,0,42.51,0,94.95s42.51,94.95,94.95,94.95,94.95-42.51,94.95-94.95S147.39,0,94.95,0Zm10.69,143.57c0,4.7-3.81,8.51-8.51,8.51h-4.35c-4.7,0-8.51-3.81-8.51-8.51v-65.69c0-4.7,3.81-8.51,8.51-8.51h4.35c4.7,0,8.51,3.81,8.51,8.51v65.69Zm-10.69-82.16c-7.26,0-13.14-5.88-13.14-13.14s5.88-13.14,13.14-13.14,13.14,5.88,13.14,13.14-5.88,13.14-13.14,13.14Z"
        />
      </svg>
      <span class="ml-[12px] text-white">{{ alertStore.message }}</span>
    </div>
  </div>

  <main class="!w-screen overflow-x-clip">
    <img
      src="/farmbg.svg"
      id="bg"
      alt=""
      class="fixed top-0 -z-10 object-cover"
    />
    <div>
      <BgCloud
        v-for="i of clouds"
        :key="i.id"
        class="float fixed -right-36 -z-10 h-14 select-none"
        :style="{
          top: i.top,
        }"
      />
    </div>
    <RouterView />
  </main>
</template>

<style>
#bg {
  width: 100vw;
  height: 100vh;
}

@keyframes cloud-float {
  0% {
    transform: translateX(150px);
  }
  100% {
    transform: translateX(calc(-100vw - 150px));
  }
}

.float {
  animation: cloud-float 50s linear infinite;
}
</style>
