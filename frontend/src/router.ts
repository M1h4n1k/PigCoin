import { createWebHistory, createRouter } from "vue-router";

const Home = () => import("@/views/Home.vue");
const Rating = () => import("@/views/Rating.vue");
const Boosts = () => import("@/views/Boosts.vue");
const Tasks = () => import("@/views/Tasks.vue");
const Frens = () => import("@/views/Frens.vue");
const Club = () => import("@/views/Club.vue");
const CreateClub = () => import("@/views/CreateClub.vue");
const MiniGame = () => import("@/views/MiniGame.vue");
const Auction = () => import("@/views/Auction.vue");

const routes = [
  { path: "/", component: Home },
  { path: "/rating", component: Rating },
  { path: "/boosts", component: Boosts },
  { path: "/tasks", component: Tasks },
  { path: "/frens", component: Frens },
  { path: "/club", component: Club },
  { path: "/createClub", component: CreateClub },
  { path: "/minigame", component: MiniGame },
  { path: "/auction", component: Auction },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, _, next) => {
  if (to.path === "/") {
    Telegram.WebApp.BackButton.hide();
  } else {
    document.body.style.overflow = "scroll";
    Telegram.WebApp.BackButton.show();
  }
  Telegram.WebApp.BackButton.onClick(() => {
    router.push("/");
  });

  next();
});

export default router;
