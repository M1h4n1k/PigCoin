import i18n from "@/i18n-setup";

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

const shareInviteLink = (userId: number, clubId?: number) => {
  let startApp = `${userId.toString(16)}`;
  if (clubId) {
    startApp += `_${(clubId * -1).toString(16)}`;
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
