from pydantic import BaseModel, ConfigDict, RootModel
from typing import Dict, List, Optional


class FlexibleModel(RootModel[Dict[str, str]]):
    pass


# UserProfile Schema
class UserProfileBase(BaseModel):
    name: str
    age: int
    weight: str
    gender: str
    experience_level: str
    activity_level: str


class UserProfileCreate(UserProfileBase):
    pass


class UserProfile(UserProfileBase):
    id: int | None = None

    model_config = ConfigDict(from_attributes=True)

# Goal Schema
class GoalBase(BaseModel):
    text: str
    choices: List[str]


class GoalCreate(GoalBase):
    pass


class Goal(GoalBase):
    id: int | None = None

    model_config = ConfigDict(from_attributes=True)

    def __repr__(self) -> str:
        return f"Goal(id={self.id!r}, text={self.text!r}, choices={self.choices!r})"


# Note Schema
class NoteBase(BaseModel):
    text: str


class NoteCreate(NoteBase):
    pass


class Note(NoteBase):
    id: int | None = None

    model_config = ConfigDict(from_attributes=True)

    def __repr__(self) -> str:
        return f"Note(id={self.id!r}, text={self.text!r})"


# WeeklySchedule Schema
class WeeklyScheduleBase(BaseModel):
    days_per_week: int
    workout_days: List[str]


class WeeklyScheduleCreate(WeeklyScheduleBase):
    pass


class WeeklySchedule(WeeklyScheduleBase):
    id: int | None = None

    model_config = ConfigDict(from_attributes=True)


# WorkoutPlan Schema
class WorkoutPlanBase(BaseModel):
    goal: str
    user_profile: UserProfileBase
    weekly_schedule: WeeklyScheduleBase


class WorkoutPlanCreate(WorkoutPlanBase):
    pass


class WorkoutPlan(WorkoutPlanBase):
    id: int | None = None

    model_config = ConfigDict(from_attributes=True)


# Exercise Schema
class ExerciseBase(BaseModel):
    name: str
    sets: int | None = None
    reps: int | None = None
    rest: str | None = None


class ExerciseCreate(ExerciseBase):
    pass


class Exercise(ExerciseBase):
    id: int | None = None

    model_config = ConfigDict(from_attributes=True)


# Workout Schema
class WorkoutBase(BaseModel):
    day: str
    focus: str
    exercises: List[ExerciseBase]


class WorkoutCreate(WorkoutBase):
    pass


class Workout(WorkoutBase):
    id: int | None = None

    model_config = ConfigDict(from_attributes=True)


# WorkoutRoutine Schema
class WorkoutRoutineBase(BaseModel):
    name: str
    description: str
    workout_plan: WorkoutPlanBase
    workouts: List[WorkoutBase]
    notes: List[str]


class WorkoutRoutineCreate(WorkoutRoutineBase):
    pass


class WorkoutRoutine(WorkoutRoutineBase):
    id: int | None = None

    model_config = ConfigDict(from_attributes=True)
