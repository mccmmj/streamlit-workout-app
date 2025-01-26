import json
import logging

from database import (
    UserProfile,
    WeeklySchedule,
    WorkoutPlan,
    Exercise,
    Workout,
    WorkoutRoutine
)
from models import (
    UserProfileBase,
    WeeklyScheduleBase,
    WorkoutPlanBase,
    ExerciseBase,
    WorkoutBase,
    WorkoutRoutineBase,
)
from models import (
    UserProfile as UserProfileModel,
    WeeklySchedule as WeeklyScheduleModel,
    WorkoutPlan as WorkoutPlanModel,
    Exercise as ExerciseModel,
    Workout as WorkoutModel,
    WorkoutRoutine as WorkoutRoutineModel,
)


log = logging.getLogger(__name__)


# Transform from pydantic model to db (SQLAlchemy.orm)
def get_workout_routines(file_path: str) -> list:
    with open(file_path) as f:
        return json.load(f)


def get_user_profile(user_profile: UserProfileBase) -> UserProfile:
    return UserProfile(
        name=user_profile.name,
        age=user_profile.age,
        weight=user_profile.weight,
        gender=user_profile.gender,
        experience_level=user_profile.experience_level,
        activity_level=user_profile.activity_level
    )


def get_weekly_schedule(weekly_schedule: WeeklyScheduleBase) -> WeeklySchedule:
    return WeeklySchedule(
        days_per_week=weekly_schedule.days_per_week,
        workout_days=weekly_schedule.workout_days
    )


def get_workout_plan(workout_plan: WorkoutPlanBase) -> WorkoutPlan:
    return WorkoutPlan(
        goal=workout_plan.goal,
        user_profile=get_user_profile(workout_plan.user_profile),
        weekly_schedule=get_weekly_schedule(workout_plan.weekly_schedule)
    )


def get_exercise(exercise: ExerciseBase) -> Exercise:
    print(f"{exercise=}")
    return Exercise(
        name=exercise.name,
        sets=exercise.sets,
        reps=exercise.reps,
        rest=exercise.rest
    )


def get_workout(workout: WorkoutBase) -> Workout:
    return Workout(
        day=workout.day,
        focus=workout.focus,
        exercises=[get_exercise(ex) for ex in workout.exercises]
    )


def get_workout_routine(workout_routine: WorkoutRoutineBase) -> WorkoutRoutine:
    return WorkoutRoutine(
        name=workout_routine.name,
        description=workout_routine.description,
        workout_plan=get_workout_plan(workout_routine.workout_plan),
        workouts=[get_workout(w) for w in workout_routine.workouts],
        notes=workout_routine.notes,
    )


def create_workout_routine(session, workout_routine: WorkoutRoutineBase) -> WorkoutRoutine:
    workoutRoutine = get_workout_routine(workout_routine)

    session.add(workoutRoutine)
    session.commit()
    session.refresh(workoutRoutine)
    print(f"{workoutRoutine=}")
    return workoutRoutine


# Transmform from db (SQLAlchemy.orm) to pydantic model
def get_user_profile_model(user_profile: UserProfile) -> UserProfileModel:
    return UserProfileModel.model_validate(user_profile)


def get_weekly_schedule_model(weekly_schedule: WeeklySchedule) -> WeeklyScheduleModel:
    return WeeklyScheduleModel.model_validate(weekly_schedule)


def get_workout_plan_model(workout_plan: WorkoutPlan) -> WorkoutPlanModel:
    return WorkoutPlanModel(
        goal=workout_plan.goal,
        user_profile=get_user_profile_model(workout_plan.user_profile),
        weekly_schedule=get_weekly_schedule_model(workout_plan.weekly_schedule)
    )


def get_exercise_model(exercise: Exercise) -> ExerciseModel:
    return ExerciseModel.model_validate(exercise)


def get_workout_model(workout: Workout) -> WorkoutModel:
    return WorkoutModel(
        day=workout.day,
        focus=workout.focus,
        exercises=[get_exercise_model(ex) for ex in workout.exercises]
    )


def get_workout_routine_model(workout_routine: WorkoutRoutine) -> WorkoutRoutineModel:
    return WorkoutRoutineModel(
        name=workout_routine.name,
        description=workout_routine.description,
        workout_plan=get_workout_plan_model(workout_routine.workout_plan),
        workouts=[get_workout_model(w) for w in workout_routine.workouts],
        notes=workout_routine.notes
    )
