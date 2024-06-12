type Club = {
  id: number;
  name: string;
  picture: string;
  membersCount: number;
  total_coins: number;
  tg_link: string;
  league: number;
  members_count: number;
};

type User = {
  tg_id: number;
  picture: string;
  username: string;
  click_price: number;
  refill_rate: number;
  current_coins: number;
  total_coins: number;
  current_energy: number;
  max_energy: number;
  turbo_available: boolean;
  free_turbo: number;
  free_refills: number;
  league: number;
  club_id?: number;
  club?: Club;
};

type UserPublic = {
  tg_id: number;
  picture: string;
  username: string;
  total_coins: number;
  league: number;
};

type Boost = {
  id: number;
  title: string;
  picture: string;
  price: number;
  count: number;
};

type Task = {
  id: number;
  title: string;
  picture: string;
  reward: number;
  link: string;
  completed: boolean;
};

type BubbleBase = {
  x: number;
  y: number;
  size: number;
};

type Bubble = BubbleBase & {
  opacity: number;
  animation: string;
  direction: string;
  speed: number;
};

type DirtyBubble = BubbleBase & {
  color: string;
  hidden: boolean;
  price: number;
  rotation: number;
};

export type { User, UserPublic, Boost, Task, Bubble, DirtyBubble, Club };
