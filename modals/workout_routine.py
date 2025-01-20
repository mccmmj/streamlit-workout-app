import logging
import json

from sqlalchemy.orm import Session

import streamlit as st

from utils import db_utils

from database import (
    EngineSingleton,
    upsert_workout_routine_all,
)
from models import (
    WorkoutRoutine as WorkoutRoutineModel,
)

log = logging.getLogger(__name__)
engine = EngineSingleton.get_instance()

def sanitize_json_data(json_data):
    try:
        json.loads(json_data)
        return json_data
    except json.JSONDecodeError as e:
        log.info("error sanitizing json: %r", e)
        sanitized_data = json_data.replace("\\", "'")
        return sanitize_json_data(sanitized_data)


@st.dialog("Accept or Reject Workout Routine")
def accept_or_reject_workout_routine(json_data):
    sanitized_json = sanitize_json_data(json_data)
    logging.debug("In accept_or_reject_workout_routine: %r", sanitized_json)
    # Parse JSON into WorkoutRoutine model
    wr_model = WorkoutRoutineModel.model_validate_json(sanitized_json)

    # Streamlit UI logic
    st.title("Workout Routine Review")

    with st.expander("Workout Plan Details", expanded=True):
        st.write(f"**Goal:** {wr_model.workout_plan.goal}")
        user_profile = wr_model.workout_plan.user_profile
        st.write(
            f"**User Profile:** "
            f"Name {user_profile.name}, Age {user_profile.age}, Gender {user_profile.gender}, Weight {user_profile.weight}, "
            f"Experience Level {user_profile.experience_level}, Activity Level {user_profile.activity_level}"
        )
        schedule = wr_model.workout_plan.weekly_schedule
        st.write(f"**Weekly Schedule:** {schedule.days_per_week} days per week on {', '.join(schedule.workout_days)}")

    with st.expander("Workouts", expanded=False):
        for workout in wr_model.workouts:
            st.write(f"### {workout.day} - {workout.focus}")
            for exercise in workout.exercises:
                st.write(f"- **{exercise.name}**: {exercise.sets} sets of {exercise.reps} reps ({exercise.rest} rest)")

    with st.expander("Notes", expanded=False):
        for note in wr_model.notes:
            st.write(f"- {note}")

    # Buttons for Accept or Reject
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Accept"):
            # Save to database if accepted
            with Session(engine) as session:
                # wr_db = db_utils.create_workout_routine(session, wr_model)
                upsert_workout_routine_all(session, wr_model)
                session.commit()

            st.success("Workout routine accepted and saved!")
            st.rerun()

    with col2:
        if st.button("Reject"):
            st.warning("Workout routine rejected.")
            st.rerun()
