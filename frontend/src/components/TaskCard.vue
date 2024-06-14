<script setup lang="ts">
defineProps({
  picture: String,
  reward: Number,
  type: String,
  completed: Boolean,
});
</script>

<template>
  <div class="flex w-full cursor-pointer items-center justify-between">
    <div class="flex items-center">
      <div
        class="toned-image-bg flex h-[70px] w-[70px] items-center justify-center rounded-xl p-2"
      >
        <img class="h-8 w-8" alt="" :src="picture" />
      </div>
      <div class="ml-3">
        <p class="text-xl font-medium">{{ $t("tasks." + type) }}</p>
        <p class="text-lg">
          +{{ reward }}
          <img class="mb-1 inline h-4 w-4" src="/pigNoseCoin.svg" alt="🐽" />
        </p>
      </div>
    </div>
    <svg
      v-if="completed"
      class="h-6 w-6"
      fill="#49e994"
      aria-hidden="true"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 123 103"
    >
      <path
        d="M4.43 63.63A14.383 14.383 0 0 1 .003 53.52a14.393 14.393 0 0 1 4.015-10.281 14.372 14.372 0 0 1 10.106-4.425 14.373 14.373 0 0 1 10.283 4.012l24.787 23.851L98.543 3.989l1.768 1.349-1.77-1.355a2.27 2.27 0 0 1 .479-.466A14.383 14.383 0 0 1 109.243.022V.018l.176.016c3.623.24 7.162 1.85 9.775 4.766a14.383 14.383 0 0 1 3.662 10.412h.004l-.016.176a14.362 14.362 0 0 1-4.609 9.632L59.011 97.11l.004.004a2.157 2.157 0 0 1-.372.368 14.392 14.392 0 0 1-9.757 3.569 14.381 14.381 0 0 1-9.741-4.016L4.43 63.63z"
      />
    </svg>
    <svg v-else height="25px" width="25px" viewBox="0 0 100 100">
      <path
        d="M40.0 21.7L65.3 47.0Q66.7 48.3 66.7 49.8Q66.7 51.3 65.7 52.7L65.7 52.7L40.3 78Q39.3 79 37.7 79.2Q36.0 79.3 34.7 78.2Q33.3 77 33.3 75.3Q33.3 73.7 34.3 72.3L34.3 72.3L56.7 50.0L34.7 28.0Q33.3 27.0 33.3 25.3Q33.3 23.7 34.3 22.3L34.3 22.3L34.7 22.0Q35.7 21.0 37.2 20.8Q38.7 20.7 40.0 21.7L40.0 21.7Z"
      ></path>
    </svg>
  </div>
</template>

<style scoped></style>
