import json
import logging

from typing import List, Optional
from pydantic import ValidationError
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from database import EngineSingleton, setup_db
from database.workout_routine_db import (
    UserProfile,
    WeeklySchedule,
    WorkoutPlan,
    Exercise,
    Workout,
    WorkoutRoutine
)
from models.workout_routine import (
    UserProfileBase,
    WeeklyScheduleBase,
    WorkoutPlanBase,
    ExerciseBase,
    WorkoutBase,
    WorkoutRoutineBase,
)

load_dotenv()

engine = EngineSingleton.get_instance()
setup_db(engine)

log = logging.getLogger(__name__)


def get_workout_routines(path: str) -> list:
    with open(path) as f:
        return json.load(f)


def get_user_profile(user_profile: UserProfileBase) -> UserProfile:
    return UserProfile(
        age=user_profile.age,
        weight=user_profile.weight,
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


def main():
    # Create database session
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Load workout routine from json
    workoutRoutines: Optional[List[WorkoutRoutineBase]] = None
    try:
        routines = get_workout_routines("data/workout_routines.json")
        for routine in routines:
            print(f"{routine=}")
            wr = WorkoutRoutineBase.model_validate(routine)
            print(f"WorkoutRoutineBase={wr}")
            if not workoutRoutines:
                workoutRoutines = []
            workoutRoutines.append(wr)
    except ValidationError as e:
        print(e)

    for wr in workoutRoutines:
        res = create_workout_routine(session, wr)
        print(f"created workout routine: {res}")


if __name__ == "__main__":
    main()
