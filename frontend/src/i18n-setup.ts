import { createI18n } from "vue-i18n";
import messagesRU from "@/locales/ru.json";
import messagesEN from "@/locales/en.json";

export default createI18n({
  legacy: false,
  locale: "ru",
  fallbackLocale: "en",
  pluralRules: {
    ru: function (choice, choicesLength) {
      if (choice % 10 === 0) {
        return 0;
      }

      const teen = choice > 10 && choice < 20;
      const endsWithOne = choice % 10 === 1;

      if (choicesLength < 4) {
        return !teen && endsWithOne ? 1 : 2;
      }
      if (!teen && endsWithOne) {
        return 1;
      }
      if (!teen && choice % 10 >= 2 && choice % 10 <= 4) {
        return 2;
      }

      return choicesLength < 4 ? 2 : 3;
    },
  },
  messages: {
    ru: messagesRU,
    en: messagesEN,
  },
});
