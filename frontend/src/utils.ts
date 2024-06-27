import i18n from "@/i18n-setup";
import { useUserStore } from "@/store.ts";

const { t } = i18n.global;

const getRandomNumber = (
  min: number,
  max: number,
  previous: number,
  delta: number,
): number => {
  let random = Math.floor(Math.random() * (max - min + 1)) + min;
  while (Math.abs(random - previous) < delta) {
    random = Math.floor(Math.random() * (max - min + 1)) + min;
  }
  return random;
};

// Make that I only pass type ("club" | "user") and it will automatically get the userId and clubId
const shareInviteLink = (type: "user" | "club") => {
  const userStore = useUserStore();
  let startApp = `${userStore.user!.tg_id.toString(16)}`;
  if (type === "club") {
    startApp += `_${(userStore.user!.club_id! * -1).toString(16)}`;
  }

  const inviteText =
    `${import.meta.env.VITE_WEBAPP_URL}?startapp=${startApp}\n\n` +
    `🎁 +${(5000).toLocaleString()} 🐽 ${t("invite.default")}\n` +
    `🎁 +${(25000).toLocaleString()} 🐽 ${t("invite.premium")}`;
  Telegram.WebApp.openTelegramLink(
    `https://t.me/share/url?url=${encodeURIComponent(inviteText)}`,
  );
};

const openLink = (url: string): void => {
  if (url.startsWith("https://t.me/")) {
    Telegram.WebApp.openTelegramLink(url);
  } else {
    Telegram.WebApp.openLink(url);
  }
};

export { getRandomNumber, openLink, shareInviteLink };
