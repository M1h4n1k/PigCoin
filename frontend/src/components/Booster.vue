<script setup lang="ts">
import IconArrowRight from "@/components/IconArrowRight.vue";

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
        class="toned-image-bg flex h-[70px] w-[70px] items-center justify-center rounded-xl p-2"
      >
        <img
          class="h-[50px] w-[50px]"
          height="50"
          width="50"
          :src="picture"
          alt="refill"
        />
      </div>
      <div class="ml-2">
        <p class="text-xl">{{ title }}</p>
        <p class="text-gray-600">
          {{ price }}
          <img class="mb-0.5 inline h-3 w-3" src="/pigNoseCoin.svg" alt="🐽" />
        </p>
      </div>
    </div>

    <IconArrowRight height="25px" width="25px" />
  </div>
</template>

<style scoped></style>
