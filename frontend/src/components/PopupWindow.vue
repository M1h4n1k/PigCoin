<script setup lang="ts">
import { ref, Ref, onMounted, onUnmounted } from "vue";

defineProps({
  header: {
    type: String,
    required: true,
  },
});
const emit = defineEmits(["close"]);

const modalContainerRef: Ref<HTMLElement | null> = ref(null);

const closePopup = (e: MouseEvent) => {
  if (
    modalContainerRef.value &&
    !modalContainerRef.value.contains(e.target as Node)
  ) {
    emit("close");
  }
};

onMounted(() => {
  document.addEventListener("mouseup", closePopup);
});

onUnmounted(() => {
  document.removeEventListener("mouseup", closePopup);
});

const slideModal = (e: TouchEvent) => {
  const currentPos = {
    y: e.touches[0].clientY,
  };

  modalContainerRef.value!.style.transitionDuration = "0s";
  modalContainerRef.value!.style.transitionTimingFunction = "linear";

  const moveCard = (e: TouchEvent) => {
    if (e.touches[0].clientY - currentPos.y < 0) return;
    modalContainerRef.value!.style.transform = `translate3d(0, ${e.touches[0].clientY - currentPos.y}px, 0)`;
  };

  document.body.addEventListener("touchmove", moveCard);
  document.body.addEventListener(
    "touchend",
    () => {
      document.body.removeEventListener("touchmove", moveCard);
      if (!modalContainerRef.value) return;
      const style = window.getComputedStyle(modalContainerRef.value);
      const matrix = new DOMMatrixReadOnly(style.transform);
      if (matrix.m42 > 30) {
        modalContainerRef.value.style.removeProperty("transition-duration");
        modalContainerRef.value.style.removeProperty(
          "transition-timing-function",
        );
        emit("close");
        return;
      }
      modalContainerRef.value.style.removeProperty("transform");
      modalContainerRef.value.style.removeProperty("transition-duration");
      modalContainerRef.value.style.removeProperty(
        "transition-timing-function",
      );
    },
    { once: true },
  );
};
</script>

<template>
  <div
    ref="modalContainerRef"
    @touchstart.prevent.stop="slideModal"
    class="fixed bottom-0 left-0 w-full rounded-t-xl border-2 bg-white pb-4 opacity-100 shadow-2xl transition-all duration-150 ease-in-out"
  >
    <p class="border-b-2 px-4 py-2 text-center text-2xl font-bold">
      {{ header }}
    </p>
    <div class="px-4 py-2">
      <slot></slot>
    </div>
  </div>
</template>

<style scoped></style>
