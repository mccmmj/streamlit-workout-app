import json
import logging

from typing import Optional
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
    WorkoutRoutineCreate,
    WorkoutRoutine as WorkoutRoutineSchema
)

load_dotenv()

engine = EngineSingleton.get_instance()
setup_db(engine)

log = logging.getLogger(__name__)

# Create database session
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Load workout routine from json
wrSchema: Optional[WorkoutRoutineCreate] = None
with open("data/workout_plans.json") as f:
    try:
        routines = json.load(f)
        print(f"{routines=}")
        wrSchema = \
            WorkoutRoutineCreate.model_validate(routines[0])
        print(f"{WorkoutRoutineSchema=}")
    except ValidationError as e:
        print(e)

# if wrSchema and .user_profile
if wrSchema:

    # workoutRoutine = WorkoutRoutine(
    #     workout_plan=wrSchema.workout_plan,
    #     workouts=wrSchema.workouts,
    #     notes=wrSchema.notes
    # )
    userProfile = UserProfile(
        age=wrSchema.workout_plan.user_profile.age,
        weight=wrSchema.workout_plan.user_profile.weight,
        experience_level=wrSchema.workout_plan.user_profile.experience_level,
        activity_level=wrSchema.workout_plan.user_profile.activity_level
    )
    weeklySchedule = WeeklySchedule(
        days_per_week=wrSchema.workout_plan.weekly_schedule.days_per_week,
        workout_days=wrSchema.workout_plan.weekly_schedule.workout_days
    )
    workoutPlan = WorkoutPlan(
        goal=wrSchema.workout_plan.goal,
        user_profile=userProfile,
        weekly_schedule=weeklySchedule
    )

    workoutRoutine = WorkoutRoutine(
        name=wrSchema.name,
        description=wrSchema.description,
        notes=wrSchema.notes,
        workout_plan=workoutPlan
    )
    for wo in wrSchema.workouts:
        workout = Workout(day=wo.day, focus=wo.focus)
        for ex in workout.exercises:
            exercise = Exercise(
                name=ex.name,
                sets=ex.sets,
                reps=ex.reps,
                rest=ex.rest
            )
            workout.exercises.append(exercise)

        workoutRoutine.workouts.append(workout)

    session.add(workoutRoutine)
    session.commit()
    session.refresh(workoutRoutine)
