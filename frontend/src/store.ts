import { defineStore } from "pinia";
import { User, UserPublic, Boost } from "@/types.ts";
import { Ref, ref } from "vue";

export const useUserStore = defineStore("user", () => {
  const user: Ref<User | null> = ref(null);
  const referrals: Ref<UserPublic[]> = ref([]);
  return { user, referrals };
});

export const useBoostsStore = defineStore("boost", () => {
  const boosts: Ref<Boost[]> = ref([]);
  return { boosts };
});

export const useRatingStore = defineStore("rating", () => {
  const userRating: Ref<{ [legionId: number]: UserPublic[] }> = ref({});
  return { userRating };
});
