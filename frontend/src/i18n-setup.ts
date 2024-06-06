import { createI18n } from "vue-i18n";
import messagesRU from "@/locales/ru.json";
import messagesEN from "@/locales/en.json";

export default createI18n({
  legacy: false,
  locale: "ru",
  fallbackLocale: "en",
  messages: {
    ru: messagesRU,
    en: messagesEN,
  },
});
