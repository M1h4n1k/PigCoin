/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {
      height: {
        "tg-screen": "min(var(--tg-viewport-stable-height), 100vh)",
      },
    },
  },
  plugins: [],
};
