import { defineStore } from "pinia";
import { User, UserPublic, Boost } from "@/types.ts";
import { Ref, ref } from "vue";

export const useUserStore = defineStore("user", () => {
  const user: Ref<User | null> = ref(null);
  const referrals: Ref<UserPublic[]> = ref([]);
  const clubMembers: Ref<UserPublic[]> = ref([]);
  return { user, referrals, clubMembers };
});

export const useBoostsStore = defineStore("boost", () => {
  const boosts: Ref<Boost[]> = ref([]);
  return { boosts };
});

export const useRatingStore = defineStore("rating", () => {
  const users: Ref<{ [legionId: number]: UserPublic[] }> = ref({});
  const clubs: Ref<{ [legionId: number]: UserPublic[] }> = ref({});
  return { users, clubs };
});
