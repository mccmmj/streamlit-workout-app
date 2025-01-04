from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from database import EngineSingleton
from database.workout_routine_db import (
    UserProfile,
    WeeklySchedule,
    WorkoutPlan,
    Exercise,
    Workout,
    WorkoutRoutine
)
from models.workout_routine import (
    UserProfile as UserProfileModel,
    WeeklySchedule as WeeklyScheduleModel,
    WorkoutPlan as WorkoutPlanModel,
    Exercise as ExerciseModel,
    Workout as WorkoutModel,
    WorkoutRoutine as WorkoutRoutineModel,
)



load_dotenv()

engine = EngineSingleton.get_instance()


def transform_user_profile(user_profile: UserProfile) -> UserProfileModel:
    return UserProfileModel.model_validate(user_profile)


def transform_weekly_schedule(weekly_schedule: WeeklySchedule) -> WeeklyScheduleModel:
    return WeeklyScheduleModel.model_validate(weekly_schedule)


def transform_workout_plan(workout_plan: WorkoutPlan) -> WorkoutPlanModel:
    return WorkoutPlanModel(
        goal=workout_plan.goal,
        user_profile=transform_user_profile(workout_plan.user_profile),
        weekly_schedule=transform_weekly_schedule(workout_plan.weekly_schedule)
    )


def transform_exercise(exercise: Exercise) -> ExerciseModel:
    return ExerciseModel.model_validate(exercise)


def transform_workout(workout: Workout) -> WorkoutModel:
    return WorkoutModel(
        day=workout.day,
        focus=workout.focus,
        exercises=[transform_exercise(ex) for ex in workout.exercises]
    )


def transform_workout_routine(workout_routine: WorkoutRoutine) -> WorkoutRoutineModel:
    return WorkoutRoutineModel(
        name=workout_routine.name,
        description=workout_routine.description,
        workout_plan=transform_workout_plan(workout_routine.workout_plan),
        workouts=[transform_workout(w) for w in workout_routine.workouts],
        notes=workout_routine.notes
    )


def main():

    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    for wr in session.query(WorkoutRoutine).all():
        res = transform_workout_routine(wr)
        print(res)


if __name__ == "__main__":
    main()
