type User = {
  tg_id: number;
  picture: string;
  username: string;
  current_coins: number;
  total_coins: number;
  current_energy: number;
  max_energy: number;
  turbo_available: boolean;
  free_turbo: number;
  free_refills: number;
  league: number;
};

type UserPublic = {
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

export type { User, UserPublic, Boost, Task };
