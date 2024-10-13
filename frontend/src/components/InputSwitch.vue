<script setup lang="ts">
defineProps({
  activeTab: {
    type: Number,
    required: true,
  },
  options: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(["update:activeTab"]);
</script>

<template>
  <div class="toned-bg flex w-fit cursor-pointer select-none rounded-2xl">
    <div
      v-for="(option, i) in options"
      :key="i"
      class="rounded-xl border-[1px] border-transparent px-3 py-2 font-medium"
      :class="{
        'toned-image-bg': activeTab === i,
      }"
      @click="emit('update:activeTab', i)"
    >
      {{ option }}
    </div>
  </div>
</template>
