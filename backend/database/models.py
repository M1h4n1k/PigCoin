from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import ForeignKey, DateTime, Text, Boolean, func, BIGINT, VARCHAR, Double
from sqlalchemy.orm import relationship, DeclarativeBase, mapped_column, Mapped
from utils import get_user_league, get_club_league


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    tg_id: Mapped[int] = mapped_column(BIGINT, unique=True, primary_key=True)
    picture: Mapped[str] = mapped_column(VARCHAR(255))
    username: Mapped[str] = mapped_column(VARCHAR(255))
    referrer_tg_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.tg_id'), index=True)
    club_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('clubs.id'), index=True)
    blocked: Mapped[bool] = mapped_column(Boolean, default=False)

    current_energy: Mapped[int] = mapped_column(BIGINT, default=1000)

    total_coins: Mapped[int] = mapped_column(BIGINT, default=0, index=True)
    current_coins: Mapped[int] = mapped_column(BIGINT, default=0)

    free_turbo: Mapped[int] = mapped_column(BIGINT, default=3, index=True)
    free_refills: Mapped[int] = mapped_column(BIGINT, default=3, index=True)

    turbo_available: Mapped[bool] = mapped_column(Boolean, default=False)

    join_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())

    @hybrid_property
    def league(self) -> int:
        return get_user_league(self.total_coins)

    boosts: Mapped['Boost'] = relationship('Boost', secondary='user_boosts')
    club: Mapped['Club'] = relationship('Club', back_populates='users')
    referrals: Mapped['User'] = relationship('User', remote_side=[referrer_tg_id])
    tasks_completed: Mapped['Task'] = relationship('Task', secondary='user_tasks')


# it's possible to do it via simple json array, since I'm not planning to add any new boosts
class Boost(Base):
    __tablename__ = 'boosts'

    id: Mapped[int] = mapped_column(BIGINT, unique=True, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    base_price: Mapped[int] = mapped_column(BIGINT)
    coins: Mapped[int] = mapped_column(BIGINT)
    picture: Mapped[str] = mapped_column(VARCHAR(255))


class UserBoost(Base):
    __tablename__ = 'user_boosts'

    user_tg_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.tg_id'), primary_key=True)
    boost_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('boosts.id'), primary_key=True)
    count: Mapped[int] = mapped_column(BIGINT, default=0)


class Club(Base):
    __tablename__ = 'clubs'

    id: Mapped[int] = mapped_column(BIGINT, unique=True, primary_key=True)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    picture: Mapped[str] = mapped_column(VARCHAR(255))
    tg_link: Mapped[str] = mapped_column(VARCHAR(255))

    total_coins: Mapped[int] = mapped_column(BIGINT, default=0)
    members: Mapped['User'] = relationship('User', back_populates='club')

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
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())


class UserTask(Base):
    __tablename__ = 'user_tasks'

    user_tg_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.tg_id'), primary_key=True)
    task_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('tasks.id'), primary_key=True)
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
