import { createWebHistory, createRouter } from "vue-router";

const Rating = () => import("@/views/Rating.vue");
const Home = () => import("@/views/Home.vue");
const Boosters = () => import("@/views/Boosters.vue");

const routes = [
  { path: "/", component: Home },
  { path: "/hello", component: Home },
  { path: "/rating", component: Rating },
  { path: "/boosters", component: Boosters },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
