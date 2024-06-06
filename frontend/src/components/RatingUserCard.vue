<script setup lang="ts">
defineProps({
  name: {
    type: String,
    required: true,
  },
  rating: {
    type: Number,
    required: true,
  },
  avatar: {
    type: String,
    required: false,
  },
  coins: {
    type: Number,
    required: true,
  },
  isYou: {
    type: Boolean,
    default: false,
  },
});
</script>

<template>
  <div class="relative flex items-center">
    <span
      class="w-14 text-center text-lg"
      :class="{
        'text-yellow-400': rating === 1,
        'text-orange-300': rating === 2,
        'text-yellow-700': rating === 3,
        'font-extrabold': rating < 4,
      }"
    >
      {{ rating }}
    </span>
    <div class="flex items-center">
      <img class="h-10 w-10 rounded-full bg-red-100" alt="" :src="avatar" />
      <div class="ml-2">
        <p class="font-medium">{{ name }}</p>
        <p class="text-gray-600">{{ coins }}🐽</p>
      </div>
    </div>
    <span v-if="isYou" class="absolute right-5 text-center font-semibold"
      >You</span
    >
  </div>
</template>

<style scoped></style>
