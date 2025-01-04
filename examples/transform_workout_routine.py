from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
from database import EngineSingleton
from database.workout_routine_db import WorkoutRoutine
from models.workout_routine import WorkoutRoutine as WorkoutRoutineSchema

load_dotenv()

engine = EngineSingleton.get_instance()

SessionLocal = sessionmaker(bind=engine)

session = SessionLocal()

for wr in session.query(WorkoutRoutine).all():
    wrSchema = WorkoutRoutineSchema.model_validate(wr)
    print(wrSchema)
