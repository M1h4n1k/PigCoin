<script setup lang="ts">
import { onUnmounted, ref } from "vue";
import { useUserStore } from "@/store";
import BgCloud from "@/components/BgCloud.vue";
import AlertToast from "@/components/AlertToast.vue";

const userStore = useUserStore();
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
  <AlertToast />

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
    transform: translateX(0px);
  }
  100% {
    transform: translateX(calc(-100vw - 150px));
  }
}

.float {
  animation: cloud-float 50s linear infinite;
}
</style>
