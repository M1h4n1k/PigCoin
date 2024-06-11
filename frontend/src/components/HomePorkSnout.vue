<script setup lang="ts">
import { ref, Ref, onMounted } from "vue";
import { useUserStore } from "@/store";
import { Bubble, DirtyBubble } from "@/types";

const userStore = useUserStore();

const cleaning = ref(false);
const container: Ref<HTMLElement | null> = ref(null);

const bubbles: Ref<Bubble[]> = ref([]); // Array to store bubble objects
const bubblesI = ref(0);
const bubblesMaxCount = 60;

const dirtyColors = ["#a4764a", "#9b7653", "#94765a", "#987654", "#a67b5b"];
const dirtyBubbles: Ref<DirtyBubble[]> = ref([]); // Array to store bubble objects
const dirtyBubblesCleanedCount = ref(0); // helps to delay the next bubble appearance

const coinsCollectedBatch = ref(0);

const touchMove = (e: TouchEvent | MouseEvent) => {
  if (!cleaning.value) return;
  e.preventDefault();

  // Calculate bubble position relative to cursor
  const x = e.clientX - container.value!.getBoundingClientRect().left;
  const y = e.clientY - container.value!.getBoundingClientRect().top;
  const bubbleSize = Math.random() * 15 + 15; // Random bubble size (15px - 30px)
  const speed = Math.random() * 0.5 + 0.5; // Random speed (0.5 - 1)

  if (bubblesI.value >= bubblesMaxCount) {
    bubblesI.value = 0;
  }
  if (bubbles.value.length < bubblesMaxCount) {
    bubbles.value.push({} as Bubble);
  }

  bubbles.value[bubblesI.value] = {
    x,
    y,
    size: bubbleSize,
    opacity: 1, // Initial opacity
    animation: `bubble-animation ${bubbleSize * 0.2}s ease-in-out 1 forwards`, // Animation duration based on size
    direction: `ray(${Math.random() * 360}deg at ${x}px ${y}px)`, // Initial direction
    speed,
  };
  bubblesI.value++;
};

const cleanDirtyBubble = (index: number) => {
  if (!cleaning.value || dirtyBubbles.value[index].hidden) {
    return;
  }
  if (collectCoin()) {
    dirtyBubbles.value[index].price = userStore.user!.click_price;
  }
  dirtyBubbles.value[index].hidden = true;
  setTimeout(
    () => {
      if (container.value === null) return;
      dirtyBubbles.value[index] = {
        x: 60 + Math.random() * (container.value.clientWidth - 170),
        y: 100 + Math.random() * (container.value.clientWidth - 200),
        size: Math.random() * 20 + 20, // Random bubble size (20px - 40px)
        color: dirtyColors[Math.floor(Math.random() * dirtyColors.length)],
        hidden: false,
        price: 0,
        rotation: Math.random() * 360,
      };
      dirtyBubblesCleanedCount.value--;
    },
    600 + dirtyBubblesCleanedCount.value * 100,
  );
  dirtyBubblesCleanedCount.value++;
};

const collectCoin = () => {
  if (userStore.user!.current_energy < userStore.user!.click_price) {
    return false;
  }
  userStore.user!.current_energy -= userStore.user!.click_price;
  userStore.user!.current_coins += userStore.user!.click_price;
  coinsCollectedBatch.value += userStore.user!.click_price;
  return true;
};

const collectCoinsBatch = () => {
  if (coinsCollectedBatch.value === 0) {
    return;
  }
  fetch(import.meta.env.VITE_API_URL + "/game/collectCoins", {
    method: "POST",
    credentials: "include",
    body: JSON.stringify({ coins: coinsCollectedBatch.value }),
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      userStore.user = data;
      coinsCollectedBatch.value = 0;
    });
};

onMounted(() => {
  setInterval(collectCoinsBatch, 5000);
  for (let i = 0; i < 10; i++) {
    dirtyBubbles.value.push({
      x: 80 + Math.random() * (container.value!.clientWidth - 160),
      y: 100 + Math.random() * (container.value!.clientWidth - 200),
      size: Math.random() * 20 + 20, // Random bubble size (20px - 40px)
      color: dirtyColors[Math.floor(Math.random() * dirtyColors.length)],
      hidden: false,
      price: 0,
      rotation: Math.random() * 360,
    });
  }
});
</script>

<template>
  <div
    ref="container"
    class="relative overflow-hidden"
    @mousedown="cleaning = true"
    @mousemove="touchMove"
    @mouseup="cleaning = false"
    @touchstart="cleaning = true"
    @touchmove="touchMove"
    @touchend="cleaning = false"
  >
    <div
      class="bubble pointer-events-none absolute z-20 rounded-full border border-blue-300 border-opacity-50 bg-white"
      v-for="(bubble, ind) in bubbles"
      :key="bubble.x * 1000 + bubble.y * 100 + ind * 10 + bubble.size"
      :style="{
        left: bubble.x - bubble.size / 2 + 'px',
        top: bubble.y - bubble.size / 2 + 'px',
        width: bubble.size + 'px',
        height: bubble.size + 'px',
        offsetPath: bubble.direction,
      }"
    ></div>

    <div
      class="absolute z-10 flex select-none rounded-full border-black border-opacity-50 transition-opacity duration-500"
      v-for="(dirtyBubble, ind) in dirtyBubbles"
      :key="ind"
      @mousedown="(e) => e.preventDefault()"
      @mouseover="cleanDirtyBubble(ind)"
      @touchmove="cleanDirtyBubble(ind)"
      :style="{
        left: dirtyBubble.x - dirtyBubble.size / 2 + 'px',
        top: dirtyBubble.y - dirtyBubble.size / 2 + 'px',
        width: '100px', //dirtyBubble.size + 'px',
        height: '100px', // dirtyBubble.size + 'px',
        opacity: dirtyBubble.hidden ? 0 : 1,
        pointerEvents: dirtyBubble.hidden ? 'none' : 'auto',
        // backgroundColor: dirtyBubble.color,
        // transform: `rotate(${dirtyBubble.rotation}deg)`,
      }"
    >
      <div class="relative h-full w-full">
        <img class="h-auto w-full" src="/mud2.png" alt="" />
      </div>
    </div>

    <!-- If I move it to the bubble component it will inherit the opacity and disappear quite quickly -->
    <span
      v-for="(dirtyBubble, ind) in dirtyBubbles"
      :key="ind"
      class="number absolute z-30 w-fit select-none text-2xl font-bold text-white"
      :style="{
        left: dirtyBubble.x - dirtyBubble.size / 2 + 'px',
        top: dirtyBubble.y - dirtyBubble.size / 2 + 'px',
        display: dirtyBubble.hidden ? 'inline' : 'none',
      }"
    >
      +{{ dirtyBubble.price }}
    </span>

    <img
      class="h-auto w-full"
      src="/pigNose.webp"
      alt="None"
      draggable="false"
    />
  </div>
</template>

<style scoped>
.bubble {
  animation: bubble-animation forwards 0.8s ease-in-out; /* Initial animation */
}
/* animation: move 3000ms infinite alternate ease-in-out; */
@keyframes bubble-animation {
  from {
    offset-distance: 0;
    opacity: 1;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(2); /* Adjust scaling for expansion effect */
    offset-distance: 40%;
    display: none;
  }
}

.number {
  text-shadow:
    -2px 0 black,
    0 2px black,
    2px 0 black,
    0 -2px black;
  animation: number-animation forwards 1s ease-in-out; /* Initial animation */
}

@keyframes number-animation {
  from {
    transform: translateY(0);
  }
  to {
    opacity: 0;
    transform: translateY(-80px);
  }
}
</style>
