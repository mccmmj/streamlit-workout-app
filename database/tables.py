from typing import List
from typing import Optional
from sqlalchemy import JSON
from sqlalchemy import UniqueConstraint
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


class UserProfile(Base):
    __tablename__ = "user_profile"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    age: Mapped[int]
    weight: Mapped[str]
    gender: Mapped[str]
    experience_level: Mapped[str]
    activity_level: Mapped[str]

    goal: Mapped["Goal"] = relationship(back_populates="user_profile")

    notes: Mapped[list["Note"]] = relationship(back_populates="user_profile")

    workout_plans: Mapped[List["WorkoutPlan"]] = relationship(
        back_populates="user_profile"
    )

    def __repr__(self) -> str:
        return f"UserProfile(id={self.id!r}, name={self.name!r}, age={self.age!r}, weight={self.weight!r}, gender={self.gender!r}, experience_level={self.experience_level!r}, activity_level={self.activity_level!r})"


class Goal(Base):
    __tablename__ = "user_goal"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str]
    choices: Mapped[list[str]] = mapped_column(JSON, nullable=True)

    user_profile_id = mapped_column(ForeignKey("user_profile.id"))

    user_profile: Mapped["UserProfile"] = relationship(
        back_populates="goal"
    )

    def __repr__(self) -> str:
        return f"Goal(id={self.id!r}, text={self.text!r}, choices={self.choices!r})"


class Note(Base):
    __tablename__ = "user_note"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    text: Mapped[str]

    user_profile_id = mapped_column(ForeignKey("user_profile.id"))

    user_profile: Mapped["UserProfile"] = relationship(
        back_populates="notes"
    )

    def __repr__(self) -> str:
        return f"Note(id={self.id!r}, text={self.text!r})"


class WeeklySchedule(Base):
    __tablename__ = "weekly_schedule"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    days_per_week: Mapped[int]
    workout_days: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    workout_plans: Mapped[List["WorkoutPlan"]] = relationship(
        back_populates="weekly_schedule"
    )

    def __repr__(self) -> str:
        return f"WeeklySchedule(id={self.id!r}, days_per_week={self.days_per_week!r}, workout_days={self.workout_days!r})"


class WorkoutPlan(Base):
    __tablename__ = "workout_plan"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    goal: Mapped[str]

    user_profile_id = mapped_column(ForeignKey("user_profile.id"))
    weekly_schedule_id = mapped_column(ForeignKey("weekly_schedule.id"))

    user_profile: Mapped["UserProfile"] = relationship(
        back_populates="workout_plans"
    )
    weekly_schedule: Mapped["WeeklySchedule"] = relationship(
        back_populates="workout_plans"
    )
    workout_routine: Mapped["WorkoutRoutine"] = relationship(
        back_populates="workout_plan"
    )

    def __repr__(self) -> str:
        return f"WorkoutPlan(id={self.id!r}, goal={self.goal!r})"


class WorkoutRoutine(Base):
    __tablename__ = "workout_routine"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    description: Mapped[str]
    notes: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    workout_plan_id = mapped_column(ForeignKey("workout_plan.id"))

    workout_plan: Mapped[WorkoutPlan] = relationship(
        back_populates="workout_routine"
    )
    workouts: Mapped[List["Workout"]] = relationship(
        back_populates="workout_routine"
    )

    def __repr__(self) -> str:
        return f"WorkoutRoutine(id={self.id!r}, name={self.name!r}, description={self.description!r}, notes={self.notes!r})"


class Workout(Base):
    __tablename__ = "workout"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    day: Mapped[str]
    focus: Mapped[str]

    workout_routine_id = mapped_column(ForeignKey("workout_routine.id"))

    workout_routine: Mapped["WorkoutRoutine"] = relationship(back_populates="workouts")
    exercises: Mapped[List["Exercise"]] = relationship(back_populates="workout")


    def __repr__(self) -> str:
        return f"Workout(id={self.id!r}, day={self.day!r}, focus={self.focus!r})"


class Exercise(Base):
    __tablename__ = "exercise"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    name: Mapped[str]
    sets: Mapped[int] = mapped_column(nullable=True)
    reps: Mapped[int] = mapped_column(nullable=True)
    rest: Mapped[str] = mapped_column(nullable=True)

    workout_id = mapped_column(ForeignKey("workout.id"))

    workout: Mapped[List["Workout"]] = relationship(back_populates="exercises")

    def __repr__(self) -> str:
        return f"Exercise(id={self.id!r}, name={self.name!r}, sets={self.sets!r}, reps={self.reps!r}, rest={self.rest!r})"



