<script setup lang="ts">
import HomeSquadHeader from "@/components/HomeSquadHeader.vue";
import HomeUserStatsHeader from "@/components/HomeUserStatsHeader.vue";
import HomePorkSnout from "@/components/HomePorkSnout.vue";
import HomeFooterActions from "@/components/HomeFooterActions.vue";
</script>

<template>
  <div id="container" class="flex h-screen flex-col justify-between pb-8 pt-6">
    <div class="px-3">
      <HomeSquadHeader />
      <HomeUserStatsHeader class="mt-6" />
    </div>
    <HomePorkSnout />
    <HomeFooterActions class="px-3" />
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
