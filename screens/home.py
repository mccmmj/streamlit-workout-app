import logging
import streamlit as st

from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional

from database import EngineSingleton
from database import Goal, Note, UserProfile
from database import (
    upsert_user_profile,
    upsert_goal,
    upsert_note,
)
from models import UserProfile as UserProfileModel
from models import Goal as GoalModel
from models import Note as NoteModel

log = logging.getLogger(__name__)
engine = EngineSingleton.get_instance()
session = Session(engine)

if "shared_user_profile" not in st.session_state:
    st.session_state.shared_user_profile = None

if "shared_goal" not in st.session_state:
    st.session_state.shared_goal = None

if "shared_notes" not in st.session_state:
    st.session_state.shared_notes = None

st.title("User Profile")

# Create a select box for the user to choose a profile
select_stmt = select(UserProfile).order_by(UserProfile.name)
userProfiles = {
    f"{u.id}: {u.name} - age {u.age}": u for u in session.scalars(select_stmt).all()
}
log.info(f"Home: {userProfiles=}")
selected_profile_label = st.selectbox("Select Profile", list(userProfiles.keys()))

# Display and update user profile
user_profile = (
    UserProfileModel.model_validate(userProfiles[selected_profile_label])
    if selected_profile_label
    else UserProfileModel(
        name="",
        age=25,
        weight="70 kg",
        gender="Male",
        experience_level="Beginner",
        activity_level="Sedentary",
    )
)

st.session_state.shared_user_profile = user_profile

name = st.text_input("Name", value=user_profile.name)
age = st.number_input("Age", value=int(user_profile.age))
weight = st.text_input("Weight", value=user_profile.weight)
gender = st.selectbox(
    "Gender",
    ["Male", "Female"],
    index=["Male", "Female"].index(user_profile.gender),
)
activity_level = st.selectbox(
    "Activity Level",
    ["Sedentary", "Moderate", "Active"],
    index=["Sedentary", "Moderate", "Active"].index(user_profile.activity_level),
)
experience_level = st.selectbox(
    "Experience Level",
    ["Beginner", "Intermediate", "Advanced"],
    index=["Beginner", "Intermediate", "Advanced"].index(user_profile.experience_level),
)

goal_model: Optional[GoalModel] = None
goal_stmt = select(Goal).where(Goal.user_profile_id == user_profile.id)
goal_obj = session.scalars(goal_stmt).one()
if goal_obj:
    goal_model = GoalModel.model_validate(goal_obj)

if not goal_model:
    goal_model = GoalModel(
        text="Muscle Gain",
        choices=[
            "Weight Loss",
            "Muscle Gain",
            "Improving Balance",
            "Build Strength",
            "Toning Up",
            "Boosting Energy",
            "Improving Sleep",
            "Improving mood and self-confidence",
            "Lowering the risk of many health  conditions",
            "Increasing resting metabolism",
        ],
    )

goal_model.text = st.selectbox(
    "Goal", goal_model.choices, index=goal_model.choices.index(goal_model.text)
)
st.session_state.shared_goal = goal_model.text

# Suplementary user input (notes)
note_model: Optional[NoteModel] = None
note_stmt = select(Note).where(Note.user_profile_id == user_profile.id)
for note_obj in session.scalars(note_stmt).all():
    note_model = NoteModel.model_validate(note_obj)

note_value = note_model.text if note_model else ""
note_text = st.text_area(
    "Enter any health conditions or notes:",
    value=note_value,
    placeholder="e.g., knee injury, prefer low-impact exercises",
)
st.session_state.shared_notes = note_text.split("\n")


if st.button("Update Profile"):
    # Upsert UserProfile
    userProfile = upsert_user_profile(session, dict(
        name=name,
        age=age,
        weight=weight,
        gender=gender,
        experience_level=experience_level,
        activity_level=activity_level,
    ))
    user_profile = UserProfileModel.model_validate(userProfile)
    st.session_state.shared_user_profile = user_profile
    # Upsert Goal
    goal = upsert_goal(session, dict(
        text=goal_model.text,
        choices=goal_model.choices,
        user_profile_id=userProfile.id
    ))
    log.info("In Home: goal = %r", goal)
    goal_model = GoalModel.model_validate(goal)
    st.session_state.shared_goal = goal_model.text
    # Upsert Note
    note = upsert_note(session, dict(
        text=note_text,
        user_profile_id=userProfile.id
    ))
    note_model = NoteModel.model_validate(note)
    st.session_state.shared_goal = note_model.text.split("\n")
    session.commit()

    st.success("Profile updated successfully!")
