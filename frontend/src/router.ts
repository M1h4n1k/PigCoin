import { createWebHistory, createRouter } from "vue-router";

const Home = () => import("@/views/Home.vue");
const Rating = () => import("@/views/Rating.vue");
const Boosts = () => import("@/views/Boosts.vue");
const Tasks = () => import("@/views/Tasks.vue");
const Frens = () => import("@/views/Frens.vue");
const Club = () => import("@/views/Club.vue");
const MiniGame = () => import("@/views/MiniGame.vue");

const routes = [
  { path: "/", component: Home },
  { path: "/rating", component: Rating },
  { path: "/boosts", component: Boosts },
  { path: "/tasks", component: Tasks },
  { path: "/frens", component: Frens },
  { path: "/club", component: Club },
  { path: "/minigame", component: MiniGame },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
