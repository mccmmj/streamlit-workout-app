import streamlit as st
import pandas as pd

if 'shared_data' not in st.session_state:
    st.session_state.shared_data = None

st.title("User Profile")

# Load user data
users_df = pd.read_csv("data/users.csv")

# Select user (for simplicity)
username = st.selectbox("Select User", users_df["username"])

# Display and update user profile
user_data = users_df[users_df["username"] == username].iloc[0]

st.session_state.shared_data = user_data

age = st.number_input("Age", value=int(user_data["age"]))
weight = st.number_input("Weight (kg)", value=float(user_data["weight"]))
gender = st.selectbox(
    "Gender",
    ["Male", "Female"],
    index=["Male", "Female"].index(user_data["gender"]),
)
activity_level = st.selectbox(
    "Activity Level",
    ["Sedentary", "Moderate", "Active"],
    index=["Sedentary", "Moderate", "Active"].index(user_data["activity_level"]),
)
experience_level = st.selectbox(
    "Experience Level",
    ["Beginner", "Intermediate", "Advanced"],
    index=["Beginner", "Intermediate", "Advanced"].index(
        user_data["experience_level"]
    ),
)

goal = st.selectbox(
    "Goal",
    [
        "Weight Loss",
        "Muscle Gain",
        "Improving Balance",
        "Build Strength",
        "Toning Up",
        "Boosting Energy",
        "Improving Sleep",
        "Improving mood and self-confidence",
        "Lowering the risk of many health  conditions",
        "Increasing resting metabolism"
    ],
    index=[
        "Weight Loss",
        "Muscle Gain",
        "Improving Balance",
        "Build Strength",
        "Toning Up",
        "Boosting Energy",
        "Improving Sleep",
        "Improving mood and self-confidence",
        "Lowering the risk of many health  conditions",
        "Increasing resting metabolism"
    ].index(user_data["goal"]),
)


if st.button("Update Profile"):
    users_df.loc[users_df["username"] == username] = [
        username,
        age,
        weight,
        gender,
        activity_level,
        experience_level,
        goal,
    ]
    users_df.to_csv("data/users.csv", index=False)
    st.success("Profile updated successfully!")

