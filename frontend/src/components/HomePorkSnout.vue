<script setup lang="ts">
import { ref, Ref, onMounted } from "vue";

const cleaning = ref(false);
const container: Ref<HTMLElement | null> = ref(null);
const nose: Ref<HTMLElement | null> = ref(null);

type Bubble = {
  x: number;
  y: number;
  size: number;
  opacity: number;
  animation: string;
  direction: string;
  speed: number;
};

const bubbles: Ref<Bubble[]> = ref([]); // Array to store bubble objects
const bubblesI = ref(0);
const bubblesMaxCount = 100;

const squeezeWithRandomTimeout = () => {
  // Generate random timeout between 5 and 15 seconds (adjust as needed)
  const randomTimeout = Math.floor(Math.random() * (15000 - 5000 + 1)) + 5000;
  if (!nose.value) return;

  nose.value.classList.add("image-squeeze");
  setTimeout(() => {
    if (!nose.value) return;
    nose.value.classList.remove("image-squeeze");
  }, 500);

  // Schedule next iteration with random timeout
  setTimeout(squeezeWithRandomTimeout, randomTimeout);
};

onMounted(() => {
  setTimeout(() => squeezeWithRandomTimeout(), 2000);
});

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
  if (bubbles.value.length != bubblesMaxCount) {
    const lastBubble =
      bubbles.value[
        (bubblesI.value - 1 + bubbles.value.length) % bubbles.value.length
      ];
    const xN = (lastBubble.x + x) / 2;
    const yN = (lastBubble.y + y) / 2;
    bubbles.value[bubblesI.value + 1] = {
      x: xN,
      y: yN,
      size: Math.random() * 15 + 15,
      opacity: 1, // Initial opacity
      animation: `bubble-animation ${Math.random() * 15 + 15 * 0.2}s ease-in-out 1 forwards`, // Animation duration based on size
      direction: `ray(${Math.random() * 360}deg at ${xN}px ${yN}px)`, // Initial direction
      speed,
    };
    bubblesI.value++;
  }
  bubblesI.value++;
};
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
      class="bubble pointer-events-none absolute rounded-full border border-blue-300 border-opacity-50 bg-white"
      v-for="(bubble, ind) in bubbles"
      :key="bubble.x * 1000 + bubble.y * 100 + ind * 10 + bubble.size"
      :style="{
        left: bubble.x - bubble.size / 2 + 'px',
        top: bubble.y - bubble.size / 2 + 'px',
        width: bubble.size + 'px',
        height: bubble.size + 'px',
        'offset-path': bubble.direction,
      }"
    ></div>

    <img
      ref="nose"
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
  z-index: 100;
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
