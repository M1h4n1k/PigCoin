<script setup lang="ts">
import { shareInviteLink } from "@/utils.ts";
import IconArrowRight from "@/components/IconArrowRight.vue";
import IconDoneTick from "@/components/IconDoneTick.vue";

const props = defineProps({
  id: {
    type: Number,
    required: true,
  },
  picture: {
    type: String,
    required: true,
  },
  reward: {
    type: Number,
    required: true,
  },
  link: {
    type: String,
    required: false,
  },
  type: {
    type: String,
    required: true,
  },
  completed: {
    type: Boolean,
    default: false,
  },
});

const completeTask = () => {
  if (props.completed) return;

  if (props.type === "invite") {
    shareInviteLink("user");
  } else if (props.link) {
    fetch(import.meta.env.VITE_API_URL + `/tasks/${props.id}/complete`, {
      method: "POST",
      credentials: "include",
    }).then((res) => {
      if (res.ok) {
        window.location.reload(); // easiest option, instead of manually updating the store. Manual changes may become inconsistent
      }
    });
    Telegram.WebApp.openTelegramLink(props.link);
  }
};
</script>

<template>
  <div
    @click="completeTask"
    :style="{
      cursor: completed ? 'auto' : 'pointer',
    }"
    class="flex w-full items-center justify-between"
  >
    <div class="flex items-center">
      <div
        class="toned-image-bg flex h-[70px] w-[70px] items-center justify-center rounded-xl p-4"
      >
        <img class="h-full w-full" alt="" :src="picture" />
      </div>
      <div class="ml-3">
        <p class="text-xl font-medium">{{ $t("tasks." + type) }}</p>
        <p class="text-lg">
          +{{ reward }}
          <img
            class="mb-1 inline h-4 w-4"
            src="/pigNoseCoin.svg"
            draggable="false"
            alt="🐽"
          />
        </p>
      </div>
    </div>
    <IconDoneTick v-if="completed" class="h-6 w-6" />
    <IconArrowRight v-else height="25px" width="25px" />
  </div>
</template>

<style scoped></style>
