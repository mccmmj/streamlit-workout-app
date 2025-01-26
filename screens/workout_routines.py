import logging

from typing import Dict 
from sqlalchemy import select
from sqlalchemy.orm import Session

import streamlit as st

from utils import db_utils

from database import EngineSingleton
from database import WorkoutRoutine
from models import WorkoutRoutine as WorkoutRoutineModel

log = logging.getLogger(__name__)
engine = EngineSingleton.get_instance()
session = Session(engine)

# Fetch all saved workouts from the database
workout_routines: Dict[int, WorkoutRoutineModel] = {}
stmt = select(WorkoutRoutine)
for wr in session.scalars(stmt).all():
    print(f"{wr=}")
    res = db_utils.get_workout_routine_model(wr)
    print(f"{res=}")
    workout_routines[wr.id] = res

# Check if there are any workout routines in the database
if not workout_routines:
    st.warning("No workout routines found in the database.")
else:
    # Create a select box for the user to choose a workout
    workout_options = {f"{v.name}: {v.workout_plan.goal}": k for k,v in workout_routines.items()}
    selected_workout_label = st.selectbox("Select a Workout", list(workout_options.keys()))

    # Get the selected workout's ID
    selected_workout_id = workout_options[selected_workout_label]

    # Fetch details of the selected workout
    workout_routine = workout_routines[selected_workout_id]
    if workout_routine:
        # Display the workout routine details using expanders
        goal = workout_routine.workout_plan.goal
        st.title(f"{workout_routine.name} - {goal}")
        st.subheader(f"{workout_routine.description}")

        with st.expander("User Profile", expanded=True):
            user_profile = workout_routine.workout_plan.user_profile
            st.write(f"**Name:** {user_profile.name}")
            st.write(f"**Age:** {user_profile.age}")
            st.write(f"**Weight:** {user_profile.weight}")
            st.write(f"**Gender:** {user_profile.gender}")
            st.write(f"**Experience Level:** {user_profile.experience_level}")
            st.write(f"**Activity Level:** {user_profile.activity_level}")

        with st.expander("Weekly Schedule", expanded=False):
            weekly_schedule = workout_routine.workout_plan.weekly_schedule
            st.write(f"**Days per Week:** {weekly_schedule.days_per_week}")
            st.write(f"**Workout Days:** {', '.join(weekly_schedule.workout_days)}")

        with st.expander("Workouts", expanded=False):
            for workout in workout_routine.workouts:
                st.subheader(f"{workout.day} - {workout.focus}")
                for exercise in workout.exercises:
                    st.write(
                        f"- **{exercise.name}**: {exercise.sets} sets of {exercise.reps} reps ({exercise.rest} rest)"
                    )

        with st.expander("Notes", expanded=False):
            for note in workout_routine.notes:
                st.write(f"- {note}")
