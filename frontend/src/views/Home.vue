<script setup lang="ts">
import TheSquadHeader from "@/components/HomeSquadHeader.vue";
import TheUserStatsHeader from "@/components/HomeUserStatsHeader.vue";
import ThePorkSnout from "@/components/HomePorkSnout.vue";
import HomeFooterActions from "@/components/HomeFooterActions.vue";
</script>

<template>
  <div
    id="container"
    class="flex h-screen flex-col justify-between px-3 pb-8 pt-6"
  >
    <div>
      <TheSquadHeader />
      <TheUserStatsHeader class="mt-6" />
    </div>
    <ThePorkSnout />
    <HomeFooterActions />
  </div>
</template>

<!--<style scoped>-->
<!--#container {-->
<!--  background-image: url("/farm.jpg") !important;-->
<!--  background-size: cover;-->
<!--  background-position: center;-->
<!--  background-repeat: no-repeat;-->
<!--  background-attachment: fixed;-->
<!--}-->
<!--</style>-->
