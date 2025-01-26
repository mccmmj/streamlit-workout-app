import sys
import logging
import json
import pathlib

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from utils import setup_logging
from database import (
    upsert_exercise,
    upsert_weekly_schedule,
    upsert_workout,
    upsert_workout_plan,
    upsert_workout_routine,
    upsert_user_profile,
)
from database import EngineSingleton, setup_db
from models import WorkoutRoutine as WorkoutRoutineModel

setup_logging()

engine = EngineSingleton.get_instance()
setup_db(engine)

log = logging.getLogger(__name__)

# Load Workout Routine Model
wr_model: Optional[WorkoutRoutineModel] = None
json_data = pathlib.Path('examples/workout_routine.json').open().read()
log.info("json_data: %r", json_data)
wr_model = WorkoutRoutineModel.model_validate_json(json_data)
log.info("wr_model=%r", wr_model)

session = Session(engine)

# UserProfile
userProfile = upsert_user_profile(
    session, wr_model.workout_plan.user_profile.__dict__)

# WeeklySchedule
weeklySchedule = upsert_weekly_schedule(
    session, wr_model.workout_plan.weekly_schedule.__dict__)

# WorkoutPlan
workout_plan = dict(
    goal=wr_model.workout_plan.goal,
    user_profile_id=userProfile.id,
    weekly_schedule_id=weeklySchedule.id,
)
workoutPlan = upsert_workout_plan(session, workout_plan)

# WorkoutRoutine
workout_routine = dict(
    name=wr_model.name,
    description=wr_model.description,
    notes=wr_model.notes,
    workout_plan_id=workoutPlan.id,
)
workoutRoutine = upsert_workout_routine(session, workout_routine)
log.info("workoutRoutine=", workoutRoutine)

# Workout
for w in wr_model.workouts:
    wk_data = dict(
        day=w.day,
        focus=w.focus,
        workout_routine_id=workoutRoutine.id,
    )
    wk = upsert_workout(session, wk_data)
    for ex in w.exercises:
        ex_data = dict(
            name=ex.name,
            sets=ex.sets,
            reps=ex.reps,
            rest=ex.rest,
            workout_id=wk.id
        )
        ex = upsert_exercise(session, ex_data)
