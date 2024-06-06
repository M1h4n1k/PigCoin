import { createWebHistory, createRouter } from "vue-router";

const Rating = () => import("@/views/Rating.vue");
const Home = () => import("@/views/Home.vue");
const Boosts = () => import("@/views/Boosts.vue");
const Tasks = () => import("@/views/Tasks.vue");
const Frens = () => import("@/views/Frens.vue");

const routes = [
  { path: "/", component: Home },
  { path: "/hello", component: Home },
  { path: "/rating", component: Rating },
  { path: "/boosts", component: Boosts },
  { path: "/tasks", component: Tasks },
  { path: "/frens", component: Frens },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
