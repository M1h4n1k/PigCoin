<script setup lang="ts">
import { ref, Ref, onMounted } from "vue";
import { useUserStore } from "@/store";
import { Bubble, DirtyBubble } from "@/types";
import { getRandomNumber } from "@/utils";

const userStore = useUserStore();

const cleaning = ref(false);
const container: Ref<HTMLElement | null> = ref(null);
const noseElement: Ref<HTMLElement | null> = ref(null);

const bubbles: Ref<Bubble[]> = ref([]); // Array to store bubble objects
const bubblesI = ref(0);
const bubblesSkipCounter = ref(0);
const bubblesMaxCount = 60;

const dirtyColors = ["#a4764a", "#9b7653", "#94765a", "#987654", "#a67b5b"];
const dirtyBubbles: Ref<DirtyBubble[]> = ref([]); // Array to store bubble objects
const dirtyBubblesCleanedCount = ref(0); // helps to delay the next bubble appearance
const lastCleanedDirtPosition = ref<{ x: number; y: number }>({ x: 0, y: 0 });

const coinsCollectedBatch = ref(0);

const touchMove = (e: TouchEvent | MouseEvent) => {
  if (!cleaning.value) return;

  bubblesSkipCounter.value++;
  // if (bubblesSkipCounter.value % 2 === 0) return;
  bubblesSkipCounter.value %= 2 * 17;

  // Calculate bubble position relative to cursor
  const clientX = "touches" in e ? e.touches[0].clientX : e.clientX;
  const clientY = "touches" in e ? e.touches[0].clientY : e.clientY;
  const x = clientX - container.value!.getBoundingClientRect().left;
  const y = clientY - container.value!.getBoundingClientRect().top;
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

  for (let i = 0; i < dirtyBubbles.value.length; i++) {
    if (dirtyBubbles.value[i].hidden) {
      continue;
    }
    const dx = dirtyBubbles.value[i].x - x;
    const dy = dirtyBubbles.value[i].y - y;
    const distance = Math.sqrt(dx * dx + dy * dy);
    if (distance < dirtyBubbles.value[i].size / 2) {
      cleanDirtyBubble(i);
    }
  }

  bubblesI.value++;
};

const cleanDirtyBubble = (index: number) => {
  if (!cleaning.value || dirtyBubbles.value[index].hidden) {
    return;
  }
  if (collectCoin()) {
    dirtyBubbles.value[index].price = userStore.user!.click_price;
  }
  Telegram.WebApp.HapticFeedback.impactOccurred("light");
  dirtyBubbles.value[index].hidden = true;
  setTimeout(
    () => {
      if (noseElement.value === null) return;
      lastCleanedDirtPosition.value = {
        x: getRandomNumber(
          80,
          noseElement.value.clientWidth - 80,
          lastCleanedDirtPosition.value.x,
          50,
        ),
        y: getRandomNumber(
          50,
          noseElement.value.clientWidth - 100,
          lastCleanedDirtPosition.value.x,
          50,
        ),
      };
      dirtyBubbles.value[index] = {
        x: lastCleanedDirtPosition.value.x,
        y: lastCleanedDirtPosition.value.y,
        size: 100, // Random bubble size (20px - 40px)
        color: dirtyColors[Math.floor(Math.random() * dirtyColors.length)],
        hidden: false,
        price: 0,
        rotation: Math.random() * 360,
      };
      dirtyBubblesCleanedCount.value--;
    },
    300 + dirtyBubblesCleanedCount.value * 100,
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
  let x = 0;
  let y = 0;
  for (let i = 0; i < 10; i++) {
    x = getRandomNumber(80, noseElement.value!.clientWidth - 80, x, 50);
    y = getRandomNumber(50, noseElement.value!.clientWidth - 100, y, 50);
    dirtyBubbles.value.push({
      x: x,
      y: y,
      size: Math.random() * 20 + 30, // Random bubble size (30px - 50px)
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
    class="relative overflow-y-visible px-4 py-8"
    @mousedown="cleaning = true"
    @mousemove.prevent="touchMove"
    @mouseup="cleaning = false"
    @touchstart="cleaning = true"
    @touchmove.prevent="touchMove"
    @touchend="cleaning = false"
  >
    <!-- soap -->
    <img
      src="/soap.webp"
      alt=""
      class="bubble pointer-events-none absolute z-20 rounded-full bg-white/90"
      v-for="(bubble, ind) in bubbles"
      :key="bubble.x * 1000 + bubble.y * 100 + ind * 10 + bubble.size"
      :style="{
        left: bubble.x - bubble.size / 2 + 'px',
        top: bubble.y - bubble.size / 2 + 'px',
        width: bubble.size + 'px',
        height: bubble.size + 'px',
        offsetPath: bubble.direction,
      }"
    />

    <!-- dirt -->
    <img
      class="absolute z-10 flex h-auto w-full select-none rounded-full transition-opacity duration-500"
      v-for="(dirtyBubble, ind) in dirtyBubbles"
      :key="ind"
      @mouseover="cleanDirtyBubble(ind)"
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
      src="/mud.webp"
      alt=""
    />

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
      ref="noseElement"
      class="h-auto w-full"
      src="/pigNose.webp"
      alt="None"
      draggable="false"
    />
  </div>
</template>

<style scoped>
.bubble {
  animation: bubble-animation forwards 0.8s linear; /* Initial animation */
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
  animation: number-animation forwards 1s linear; /* Initial animation */
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
