type Club = {
  id: number;
  name: string;
  picture: string;
  membersCount: number;
  total_coins: number;
  tg_tag: string;
  league: number;
  members_count: number;
};

type UserPublic = {
  uid: number;
  picture: string;
  username: string;
  total_coins: number;
  league: number;
};

type User = UserPublic & {
  tg_id: number;
  click_price: number;
  refill_rate: number;
  current_coins: number;
  current_energy: number;
  last_ad_collected: number;
  max_energy: number;
  turbo_available: boolean;
  free_turbo: number;
  free_refills: number;
  club_id?: number;
  club?: Club;
  position?: number;
  position_in_club?: number;
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
  picture: string;
  reward: number;
  type: string;
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

type AdsgramController = {
  show: () => Promise<void>;
};

type Adsgram = {
  init: (options: { blockId: string; debug?: boolean }) => AdsgramController;
};

type Transaction = {
  amount: number;
  from_user: UserPublic;
  to_user: UserPublic;
  created_at: number;
};

export type {
  User,
  UserPublic,
  Boost,
  Task,
  Bubble,
  DirtyBubble,
  Club,
  Transaction,
  Adsgram,
  AdsgramController,
};
