<script setup lang="ts">
import { onUnmounted } from "vue";
import { useUserStore } from "@/store";

const userStore = useUserStore();
const refillEnergy = () => {
  userStore.user!.current_energy = Math.min(
    userStore.user!.max_energy,
    userStore.user!.current_energy + userStore.user!.refill_rate,
  );
};

const refillInterval = setInterval(() => refillEnergy(), 1000);
onUnmounted(() => clearInterval(refillInterval));
</script>

<template>
  <main>
    <RouterView />
  </main>
</template>
