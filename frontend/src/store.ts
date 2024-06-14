import { defineStore } from "pinia";
import { User, UserPublic, Boost, Task, Club } from "@/types.ts";
import { Ref, ref } from "vue";

export const useUserStore = defineStore("user", () => {
  const user: Ref<User | null> = ref(null);
  const referrals: Ref<UserPublic[]> = ref([]);
  const clubMembers: Ref<UserPublic[]> = ref([]);
  const clubMembersLoaded: Ref<boolean> = ref(false);
  const autoCoins: Ref<number | null> = ref(null);
  return { user, referrals, clubMembers, clubMembersLoaded, autoCoins };
});

export const useBoostsStore = defineStore("boost", () => {
  const boosts: Ref<Boost[]> = ref([]);
  return { boosts };
});

export const useRatingStore = defineStore("rating", () => {
  const users: Ref<{
    [legionId: number]: {
      data: UserPublic[];
      loaded: boolean;
    };
  }> = ref({});
  const clubs: Ref<{
    [legionId: number]: {
      data: Club[];
      loaded: boolean;
    };
  }> = ref({});
  return { users, clubs };
});

export const useTasksStore = defineStore("rating", () => {
  const tasks: Ref<Task[]> = ref([]);
  return { tasks };
});
