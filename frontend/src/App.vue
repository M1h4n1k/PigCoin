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
    class="pointer-events-none fixed top-3 z-50 flex w-full items-center justify-center px-2 opacity-0 transition-opacity duration-300"
    :class="{
      '!opacity-100': alertStore.isDisplayed,
    }"
  >
    <div
      class="flex h-[45px] w-full select-none items-center rounded-xl bg-gray-800 pl-2"
    >
      <svg
        fill="#fff"
        v-if="alertStore.type === 'error'"
        height="25"
        width="25"
        viewBox="0 0 100 100"
      >
        <path
          d="M50.0 44.0L72.0 22.0Q73.3 20.7 75.0 20.7Q76.7 20.7 78.0 22.0Q79.3 23.3 79.3 25.0Q79.3 26.7 78.0 28.0L78.0 28.0L56.0 50.0L78.0 72Q79.3 73.3 79.3 75Q79.3 76.7 78.0 78Q76.7 79.3 75.0 79.3Q73.3 79.3 72.0 78L72.0 78L50.0 56.0L28.0 78Q26.7 79.3 25.0 79.3Q23.3 79.3 22.0 78Q20.7 76.7 20.7 75Q20.7 73.3 22.0 72L22.0 72L44.0 50.0L22.0 28.0Q20.7 26.7 20.7 25.0Q20.7 23.3 22.0 22.0Q23.3 20.7 25.0 20.7Q26.7 20.7 28.0 22.0L28.0 22.0L50.0 44.0Z"
        ></path>
      </svg>
      <svg
        v-else-if="alertStore.type === 'info'"
        height="25"
        width="25"
        class="ml-[15px]"
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 189.9 189.9"
      >
        <path
          fill="#fff"
          d="m94.95,0C42.51,0,0,42.51,0,94.95s42.51,94.95,94.95,94.95,94.95-42.51,94.95-94.95S147.39,0,94.95,0Zm10.69,143.57c0,4.7-3.81,8.51-8.51,8.51h-4.35c-4.7,0-8.51-3.81-8.51-8.51v-65.69c0-4.7,3.81-8.51,8.51-8.51h4.35c4.7,0,8.51,3.81,8.51,8.51v65.69Zm-10.69-82.16c-7.26,0-13.14-5.88-13.14-13.14s5.88-13.14,13.14-13.14,13.14,5.88,13.14,13.14-5.88,13.14-13.14,13.14Z"
        />
      </svg>
      <span class="ml-[5px] text-white">{{ alertStore.message }}</span>
    </div>
  </div>

  <main class="!w-screen overflow-x-clip">
    <img
      src="/farmbg.svg"
      id="bg"
      alt=""
      draggable="false"
      class="fixed top-0 -z-10 select-none object-cover"
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
