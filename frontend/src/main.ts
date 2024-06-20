import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router";
import i18n from "./i18n-setup";
import { createPinia } from "pinia";
import { useUserStore } from "./store";

const pinia = createPinia();
const tg_data = `"{\\"query_id\\":\\"AAGlqEg-AAAAAKWoSD7Nrd-w\\",\\"user\\":{\\"id\\":1044949157,\\"first_name\\":\\"Mihanik\\",\\"last_name\\":\\"\\",\\"username\\":\\"M1h4n1k\\",\\"language_code\\":\\"ru\\",\\"allows_write_to_pm\\":true},\\"auth_date\\":\\"1717841167\\",\\"hash\\":\\"80d64aa2bfcebc8eb4997fc0d992bed0579fd1d9e1b3325ecf5c19bd1fbe126e\\"}"`;

function jsonEscapeUTF(s: string) {
  return s.replace(
    /[^\x20-\x7F]/g,
    (x) => "\\u" + ("000" + x.codePointAt(0)!.toString(16)).slice(-4),
  );
}

const app = createApp(App).use(router).use(pinia).use(i18n);
const userStore = useUserStore();

fetch(import.meta.env.VITE_API_URL + "/user/login", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body:
    '"' +
    jsonEscapeUTF(JSON.stringify(window.Telegram.WebApp.initDataUnsafe))
      .replace(/\\/g, "\\\\")
      .replace(/"/g, '\\"') +
    '"',
  credentials: "include",
})
  .then((response) => response.json())
  .then((data) => {
    userStore.user = data;
    app.mount("#app");
  })
  .catch((error) => console.error(error));
