import logging

from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
from sqlalchemy import create_engine
from config.settings import settings
from database.tables import (
    Base,
    Goal,
    Note,
    UserProfile,
    Exercise,
    WeeklySchedule,
    Workout,
    WorkoutPlan,
    WorkoutRoutine,
)
from models import WorkoutRoutine as WorkoutRoutineModel

log = logging.getLogger(__name__)


class EngineSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if EngineSingleton._instance is None:
            EngineSingleton._instance = create_engine(
                settings.DATABASE_URL, echo=True
            )
        return EngineSingleton._instance


# Access the single engine instance
"""
engine = EngineSingleton.get_instance()
with engine.connect() as connection:
    result = connection.execute("SELECT 'Hello, Singleton!'")
    print(result.all())
"""


def setup_db(engine):
    Base.metadata.create_all(engine)


def upsert_weekly_schedule(session, weekly_schedule: dict) -> WeeklySchedule:
    stmt = sqlite_upsert(WeeklySchedule).values(weekly_schedule)
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_=dict(
            days_per_week=weekly_schedule["days_per_week"],
            workout_days=weekly_schedule["workout_days"],
        )
    )
    res = session.scalars(
        stmt.returning(WeeklySchedule), execution_options={"populate_existing": True}
    )
    return res.all()[0]


def upsert_workout_plan(session, workout_plan: dict) -> WorkoutPlan:
    stmt = sqlite_upsert(WorkoutPlan).values(workout_plan)
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_=dict(
            goal=workout_plan["goal"],
            user_profile_id=workout_plan["user_profile_id"],
            weekly_schedule_id=workout_plan["weekly_schedule_id"],
        )
    )
    res = session.scalars(
        stmt.returning(WorkoutPlan), execution_options={"populate_existing": True}
    )
    return res.all()[0]


def upsert_workout_routine(session, workout_routine: dict) -> WorkoutRoutine:
    stmt = sqlite_upsert(WorkoutRoutine).values(workout_routine)
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_=dict(
            name=workout_routine["name"],
            description=workout_routine["description"],
            notes=workout_routine["notes"],
            workout_plan_id=workout_routine["workout_plan_id"],
        )
    )
    res = session.scalars(
        stmt.returning(WorkoutRoutine), execution_options={"populate_existing": True}
    )
    return res.all()[0]


def upsert_exercise(session, exercise: dict) -> Exercise:
    stmt = sqlite_upsert(Exercise).values(exercise)
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_=dict(
            name=exercise["name"],
            sets=exercise["sets"],
            reps=exercise["reps"],
            rest=exercise["rest"],
        )
    )
    res = session.scalars(
        stmt.returning(Exercise), execution_options={"populate_existing": True}
    )
    return res.all()[0]


def upsert_workout(session, workout: dict) -> Workout:
    stmt = sqlite_upsert(Workout).values(workout)
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_=dict(
            day=workout["day"],
            focus=workout["focus"],
            workout_routine_id=workout["workout_routine_id"],
        )
    )
    res = session.scalars(
        stmt.returning(Workout), execution_options={"populate_existing": True}
    )
    return res.all()[0]


def upsert_user_profile(session, user_profile: dict) -> UserProfile:
    stmt = sqlite_upsert(UserProfile).values(user_profile)
    stmt = stmt.on_conflict_do_update(
        index_elements=["name"],
        set_=dict(
            age=user_profile["age"],
            weight=user_profile["weight"],
            gender=user_profile["gender"],
            experience_level=user_profile["experience_level"],
            activity_level=user_profile["activity_level"],
        )
    )
    res = session.scalars(
        stmt.returning(UserProfile), execution_options={"populate_existing": True}
    )
    return res.all()[0]


def upsert_goal(session, goal: dict) -> Goal:
    log.debug("In upsert_goal: goal=%r", goal)
    stmt = sqlite_upsert(Goal).values(goal)
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_=dict(
            text=goal["text"],
            choices=goal["choices"],
            user_profile_id=goal["user_profile_id"]
        ),
    )
    res = session.scalars(
        stmt.returning(Goal), execution_options={"populate_existing": True}
    )
    #session.commit()
    return res.all()[0]


def upsert_note(session, note: dict) -> Note:
    stmt = sqlite_upsert(Note).values(note)
    stmt = stmt.on_conflict_do_update(
        index_elements=["id"],
        set_=dict(
            text=note["text"],
            user_profile_id=note["user_profile_id"]
        )
    )
    res = session.scalars(
        stmt.returning(Note), execution_options={"populate_existing": True}
    )
    # session.commit()
    return res.all()[0]


def upsert_workout_routine_all(session, wr_model: WorkoutRoutineModel) -> None:

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
