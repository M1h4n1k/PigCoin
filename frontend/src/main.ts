import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router";
import i18n from "./i18n-setup";
import { createPinia } from "pinia";
import { useUserStore, useAlertStore } from "./store";

const pinia = createPinia();

function jsonEscapeUTF(s: string) {
  return s.replace(
    /[^\x20-\x7F]/g,
    (x) => "\\u" + ("000" + x.codePointAt(0)!.toString(16)).slice(-4),
  );
}

const app = createApp(App).use(router).use(pinia).use(i18n);
const userStore = useUserStore();

app.mount("#app");

fetch(import.meta.env.VITE_API_URL + "/user/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body:
    '"' +
    jsonEscapeUTF(JSON.stringify(Telegram.WebApp.initDataUnsafe))
      .replace(/\\/g, "\\\\")
      .replace(/"/g, '\\"') +
    '"',
  credentials: "include",
})
  .then((response) => response.json())
  .then((data) => {
    userStore.user = data;
  })
  .catch((error) => {
    const alertStore = useAlertStore();
    console.error(error);
    alertStore.displayAlert(error, "error", 15000);
  });
