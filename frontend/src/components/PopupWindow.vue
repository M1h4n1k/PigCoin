<script setup lang="ts">
import { ref, Ref, onMounted, onUnmounted } from "vue";

defineProps({
  header: {
    type: String,
    required: true,
  },
});
const emit = defineEmits(["close"]);

const modalEl: Ref<HTMLElement | null> = ref(null);

const closePopup = (e: MouseEvent) => {
  if (modalEl.value && !modalEl.value.contains(e.target as Node)) {
    emit("close");
  }
};

onMounted(() => {
  document.addEventListener("mouseup", closePopup);
});

onUnmounted(() => {
  document.removeEventListener("mouseup", closePopup);
});
</script>

<template>
  <div
    ref="modalEl"
    class="modal fixed bottom-0 w-full rounded-t-xl bg-white opacity-100 transition-all duration-200 ease-in-out"
  >
    <p class="border-b-2 px-4 py-2 text-center text-2xl font-bold">
      {{ header }}
    </p>
    <div class="px-4 py-2">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped>
.modal {
  animation: slideIn 0.15s ease-out;
}

@keyframes slideIn {
  0% {
    transform: translateY(100%);
  }
  100% {
    transform: translateY(0px);
  }
}
</style>
