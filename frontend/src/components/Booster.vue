<script setup lang="ts">
defineProps({
  title: String,
  picture: String,
  price: Number,
});
</script>

<template>
  <div class="flex w-full items-center justify-between rounded-2xl">
    <div class="flex items-center justify-center">
      <div
        class="flex h-[70px] w-[70px] items-center justify-center rounded-xl border p-2"
      >
        <img height="50" width="50" :src="picture" alt="refill" />
      </div>
      <div class="ml-2">
        <p class="text-xl">{{ title }}</p>
        <p class="text-gray-600">🐽{{ price }}</p>
      </div>
    </div>

    <svg height="25px" width="25px" viewBox="0 0 100 100">
      <path
        d="M40.0 21.7L65.3 47.0Q66.7 48.3 66.7 49.8Q66.7 51.3 65.7 52.7L65.7 52.7L40.3 78Q39.3 79 37.7 79.2Q36.0 79.3 34.7 78.2Q33.3 77 33.3 75.3Q33.3 73.7 34.3 72.3L34.3 72.3L56.7 50.0L34.7 28.0Q33.3 27.0 33.3 25.3Q33.3 23.7 34.3 22.3L34.3 22.3L34.7 22.0Q35.7 21.0 37.2 20.8Q38.7 20.7 40.0 21.7L40.0 21.7Z"
      ></path>
    </svg>
  </div>
</template>

<style scoped></style>
