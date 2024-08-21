from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey, DateTime, Text, Boolean, func, BIGINT, VARCHAR, Double, text, select, and_
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped, column_property
from utils import get_user_league, get_club_league, get_user_league_range

from sqlalchemy.orm import object_session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BIGINT, unique=True, primary_key=True)
    picture: Mapped[str] = mapped_column(VARCHAR(255))
    username: Mapped[str] = mapped_column(VARCHAR(255))
    referrer_tg_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey('users.tg_id', ondelete='SET NULL'), index=True, nullable=True
    )
    club_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey('clubs.id', ondelete='SET NULL'), index=True, nullable=True
    )
    club: Mapped['Club'] = relationship('Club', back_populates='members')
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    cheated_count: Mapped[int] = mapped_column(BIGINT, default=0)

    _current_energy: Mapped[int] = mapped_column(BIGINT, default=1000)
    energy_last_used: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    last_ad_collected: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime(2021, 1, 1))

    @property
    def can_collect_ad(self) -> bool:
        return (datetime.now() - self.last_ad_collected).seconds >= 60 * 72  # 20 times a day

    last_coin_collected: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    @property
    def auto_coins(self) -> int:
        if self.boosts.filter(UserBoost.boost_type == 'auto').first() is None:
            return 0

        # TODO change that every second is counted except for the first 10 mins
        hours_passed = min(
            (datetime.now() - self.last_coin_collected).seconds // 3600,
            self.boosts.filter(UserBoost.boost_type == 'auto').first().count
        )
        return hours_passed * 1000

    @hybrid_property
    def current_energy(self) -> int:
        return min(
            self.max_energy,
            self._current_energy + (datetime.now() - self.energy_last_used).seconds * self.refill_rate
        )

    @current_energy.setter
    def current_energy(self, value: int):
        self._current_energy = value
        self.energy_last_used = func.now()

    total_coins: Mapped[int] = mapped_column(BIGINT, default=0, index=True)
    current_coins: Mapped[int] = mapped_column(BIGINT, default=0)

    @hybrid_property
    def position(self) -> int:
        qr = object_session(self).query(User).filter(User.total_coins > self.total_coins)
        league_range = get_user_league_range(self.league)
        if league_range[1] is not None:
            qr = qr.filter(User.total_coins <= league_range[1])
        return qr.count() + 1

    @hybrid_property
    def position_in_club(self) -> int:
        qr = object_session(self).query(User).filter(and_(
            User.club_id == self.club_id,
            User.total_coins > self.total_coins
        ))
        return qr.count() + 1

    _free_turbo: Mapped[int] = mapped_column(BIGINT, default=3, index=True)  # 3 free turbo per day
    free_turbo_last_used: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    # so that I am able to update it programmatically without increasing the free daily count
    turbo_available: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    @hybrid_property
    def free_turbo(self) -> int:
        if datetime.now().day != self.free_turbo_last_used.day:
            self._free_turbo = 3
        return self._free_turbo

    @free_turbo.setter
    def free_turbo(self, value: int):
        self._free_turbo = value
        self.free_turbo_last_used = func.now()

    _free_refills: Mapped[int] = mapped_column(BIGINT, default=3, index=True)
    free_refills_last_used: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    @hybrid_property
    def free_refills(self) -> int:
        if datetime.now().day != self.free_refills_last_used.day:
            self._free_refills = 3
        return self._free_refills

    @free_refills.setter
    def free_refills(self, value: int):
        self._free_refills = value
        self.free_refills_last_used = func.now()

    join_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    @hybrid_property
    def league(self) -> int:
        return get_user_league(self.total_coins)

    @hybrid_property
    def max_energy(self) -> int:
        if self.boosts.filter(UserBoost.boost_type == 'capacity').first() is None:
            return 1000

        return 1000 + self.boosts.filter(UserBoost.boost_type == 'capacity').first().count * 100

    @hybrid_property
    def click_price(self) -> int:
        if self.boosts.filter(UserBoost.boost_type == 'click_price').first() is None:
            return 1

        return 1 + self.boosts.filter(UserBoost.boost_type == 'click_price').first().count

    @hybrid_property
    def refill_rate(self) -> int:
        if self.boosts.filter(UserBoost.boost_type == 'refill_rate').first() is None:
            return 1

        return 1 + self.boosts.filter(UserBoost.boost_type == 'refill_rate').first().count

    boosts: Mapped[list['UserBoost']] = relationship(
        'UserBoost', order_by='UserBoost.boost_id.asc()', lazy='dynamic'
    )

    referrals: Mapped[list['User']] = relationship(
        'User', remote_side=[referrer_tg_id], order_by='User.total_coins.desc()'
    )
    tasks_completed: Mapped[list['Task']] = relationship('Task', secondary='user_tasks')


# it's possible to do it via simple json array, since I'm not planning to add any new boosts
class Boost(Base):
    __tablename__ = 'boosts'

    id: Mapped[int] = mapped_column(BIGINT, unique=True, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(255))
    base_price: Mapped[int] = mapped_column(BIGINT)
    coins: Mapped[int] = mapped_column(BIGINT)
    picture: Mapped[str] = mapped_column(VARCHAR(255))
    type: Mapped[str] = mapped_column(VARCHAR(255))


class UserBoost(Base):
    __tablename__ = 'user_boosts'

    user_tg_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey('users.tg_id', ondelete='CASCADE'), primary_key=True
    )
    boost_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey('boosts.id', ondelete='CASCADE'), primary_key=True
    )
    count: Mapped[int] = mapped_column(BIGINT, default=0)
    boost_type: Mapped[str] = mapped_column(VARCHAR(255))
    boost: Mapped['Boost'] = relationship(
        'Boost', lazy='joined'
    )


class Club(Base):
    __tablename__ = 'clubs'

    id: Mapped[int] = mapped_column(BIGINT, unique=True, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    picture: Mapped[str] = mapped_column(VARCHAR(255))
    tg_tag: Mapped[str] = mapped_column(VARCHAR(255), unique=True, index=True)

    creator_tg_id: Mapped[int] = mapped_column(BIGINT)

    total_coins: Mapped[int] = mapped_column(BIGINT, default=0)
    members: Mapped[list['User']] = relationship(
        'User',
        back_populates='club',
        order_by='User.total_coins.desc()',
        lazy='dynamic'
    )
    members_count: Mapped[int] = mapped_column(BIGINT, default=0)

    @hybrid_property
    def league(self) -> int:
        return get_club_league(self.total_coins)


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(BIGINT, unique=True, primary_key=True)
    title: Mapped[str] = mapped_column(VARCHAR(255))
    picture: Mapped[str] = mapped_column(VARCHAR(255))
    reward: Mapped[int] = mapped_column(BIGINT)
    link: Mapped[str] = mapped_column(VARCHAR(255))
    type: Mapped[str] = mapped_column(VARCHAR(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())


class UserTask(Base):
    __tablename__ = 'user_tasks'

    user_tg_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey('users.tg_id', ondelete='CASCADE'), primary_key=True
    )
    task_id: Mapped[int] = mapped_column(
        BIGINT, ForeignKey('tasks.id', ondelete='CASCADE'), primary_key=True
    )
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
