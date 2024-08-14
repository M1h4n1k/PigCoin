import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router";
import i18n from "./i18n-setup";
import { createPinia } from "pinia";
import { useUserStore, useAlertStore } from "./store";
import VueGtag from "vue-gtag-next";

const pinia = createPinia();

function jsonEscapeUTF(s: string) {
  return s.replace(
    /[^\x20-\x7F]/g,
    (x) => "\\u" + ("000" + x.codePointAt(0)!.toString(16)).slice(-4),
  );
}

const app = createApp(App)
  .use(router)
  .use(pinia)
  .use(i18n)
  .use(VueGtag, {
    property: {
      id: "G-TPX8945YE8",
      params: {
        user_id: Telegram.WebApp.initDataUnsafe.user?.id,
        send_page_view: true,
      },
    },
  });

const userStore = useUserStore();

app.mount("#app");

document.documentElement.style.overflow = "hidden";
document.documentElement.style.height = "100dvh";

// const AdController = window.Adsgram.init({ blockId: "1129", debug: true });

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
    Telegram.WebApp.expand();
    Telegram.WebApp.enableClosingConfirmation();

    // AdController.show()
    //   .then((result) => {
    //     user watch ad till the end
    //     your code to reward user
    // })
    // .catch((result) => {
    //   user get error during playing ad or skip ad
    //   do nothing or whatever you want
    // });
    // Telegram.WebApp.MainButton.show();
    // Telegram.WebApp.MainButton.hide();
  })
  .catch((error) => {
    const alertStore = useAlertStore();
    console.error(error);
    alertStore.displayAlert(error, "error", 15000);
  });
