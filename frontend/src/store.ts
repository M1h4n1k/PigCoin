import { defineStore } from "pinia";
import { User, UserPublic, Boost, Task, Club } from "@/types.ts";
import { Ref, ref } from "vue";

export const useAlertStore = defineStore("alert", () => {
  const message: Ref<string | null> = ref(null);
  const type: Ref<string | null> = ref(null);
  const isDisplayed = ref(false);
  const _timeout: Ref<NodeJS.Timeout | null> = ref(null);

  const displayAlert = (
    _message: string,
    _type: string = "info",
    duration: number = 2000,
  ) => {
    message.value = _message;
    type.value = _type;
    isDisplayed.value = true;
    if (_timeout.value) {
      clearTimeout(_timeout.value);
    }
    _timeout.value = setTimeout(() => {
      isDisplayed.value = false;
    }, duration);
  };

  return { message, type, isDisplayed, displayAlert, _timeout };
});

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

export const useTasksStore = defineStore("tasks", () => {
  const tasks: Ref<Task[]> = ref([]);
  return { tasks };
});
