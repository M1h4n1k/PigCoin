<script setup lang="ts">
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "@/store.ts";

const userStore = useUserStore();

const router = useRouter();

const game = ref({
  score: 0,
  startTime: new Date(),
  timer: 20,
  coins: [] as {
    x: number;
    size: number;
    speed: number;
    type: number;
  }[],
});

const coinTypes = [
  {
    picture: "/pigNose.png",
    coins: 10,
  },
  {
    picture: "/pigsHead.png",
    coins: 50,
  },
  {
    picture: "/pig.png",
    coins: 100,
  },
];

let spawnCoinTimeout: ReturnType<typeof setTimeout> | undefined = undefined;
let timerSetterInterval: ReturnType<typeof setInterval> | undefined = undefined;

const spawnCoin = () => {
  const randomTimeout = Math.random() * 500 + 100;
  spawnCoinTimeout = setTimeout(spawnCoin, randomTimeout);

  if (game.value.coins.length > 10) return;

  const genType = () => {
    const random = Math.random();
    if (random < 0.7) return 0;
    if (random < 0.95) return 1;
    return 2;
  };

  const coin = {
    x: Math.random() * (window.innerWidth - 110) + 50,
    size: Math.random() * 30 + 30,
    speed: Math.random() * 3 + 4,
    type: genType(),
  };
  game.value.coins.push(coin);
};

onMounted(() => {
  spawnCoin();
  setTimeout(() => {
    clearInterval(timerSetterInterval);
    clearTimeout(spawnCoinTimeout);
    // game.value.coins = [];
    game.value.timer = 0;
  }, game.value.timer * 1000);
  timerSetterInterval = setInterval(() => {
    game.value.timer -= 1;
  }, 1000);
});

const collectPigNose = (e: Event, ind: number) => {
  e.preventDefault();
  if (game.value.timer === 0) return;
  game.value.score += coinTypes[game.value.coins[ind].type].coins;
  game.value.coins.splice(ind, 1);
};

const exitGame = () => {
  router.push("/");
  fetch(import.meta.env.VITE_API_URL + "/game/collectTurboCoins", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify({
      coins: game.value.score,
    }),
  })
    .then((res) => res.json())
    .then((data) => (userStore.user = data));
};
</script>

<template>
  <div class="relative h-tg-screen w-full p-2">
    <div
      v-if="game.timer === 0"
      class="toned-image-bg absolute left-1/2 top-1/2 z-10 flex h-48 w-80 max-w-full -translate-x-1/2 -translate-y-1/2 transform flex-col items-center justify-center rounded-xl px-10"
    >
      <div class="text-center">
        <h3 class="text-2xl font-bold">{{ $t("minigame.game_over") }}</h3>
        <p class="flex items-center justify-center text-xl">
          {{ $t("minigame.your_score") }}: {{ game.score
          }}<img src="/pigNoseCoin.svg" alt="🐽" class="ml-1 inline h-4 w-4" />
        </p>
      </div>

      <button
        @click="exitGame"
        class="mt-6 w-full rounded-full border bg-[#64b5ef] py-2 font-semibold text-white"
      >
        {{ $t("minigame.ok") }}
      </button>
    </div>

    <div
      class="toned-bg absolute right-3 top-3 z-10 flex h-16 w-fit select-none items-center justify-center rounded-xl text-2xl font-semibold"
    >
      <p class="p-2">00:{{ game.timer.toString().padStart(2, "0") }}</p>
      <div class="h-[70%] border border-gray-400/40"></div>
      <p class="flex items-center p-2">
        {{ game.score
        }}<img src="/pigNoseCoin.svg" alt="🐽" class="ml-1 inline h-5 w-5" />
      </p>
    </div>

    <img
      draggable="false"
      v-for="(coin, index) in game.coins"
      :key="
        coin.x * 10 + coin.size * 100 + coin.speed * 1000 + coin.type * 10000
      "
      @click="(e) => collectPigNose(e, index)"
      class="fall absolute -top-20 select-none"
      alt="🐽"
      :src="coinTypes[coin.type].picture"
      :style="{
        left: coin.x + 'px',
        width: 'auto',
        height: coin.size + 'px',
        animationDuration: coin.speed + 's',
        animationIterationCount: game.timer === 0 ? 1 : 'infinite',
      }"
    />
  </div>
</template>

<style scoped>
@keyframes coin-fall {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(110vh);
  }
}

.fall {
  animation: coin-fall 5s linear infinite;
}
</style>
