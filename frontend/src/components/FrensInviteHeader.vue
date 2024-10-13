<script setup lang="ts">
import { shareInviteLink } from "@/utils.ts";
</script>

<template>
  <div class="toned-bg mt-2 space-y-4 rounded-xl p-3">
    <h3 class="text-center text-2xl font-medium">{{ $t("frens.earn") }}</h3>
    <div class="flex items-center">
      <img height="50" width="50" src="/pigNose.webp" alt="" />
      <div class="ml-4">
        <p class="text-lg font-medium">{{ $t("frens.invite") }}</p>
        <p class="text-gray-600">
          {{ (2500).toLocaleString() }} {{ $t("frens.invite.desc") }}
        </p>
      </div>
    </div>

    <div class="flex items-center">
      <img height="50" width="50" src="/Telegram_Premium.png" alt="" />
      <div class="ml-4">
        <p class="text-lg font-medium leading-5">
          {{ $t("frens.premium") }}
        </p>
        <p class="text-gray-600">
          {{ (25000).toLocaleString() }} {{ $t("frens.invite.desc") }}
        </p>
      </div>
    </div>
  </div>
  <button
    @click="shareInviteLink('user')"
    class="mt-4 w-full rounded-full bg-[#2481cc] px-5 py-2 font-semibold text-white hover:!bg-[#1a8ad5]"
  >
    {{ $t("frens.invite.cta") }}
  </button>
</template>
